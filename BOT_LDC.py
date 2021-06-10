#BOT LDC

#Import
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import math
import json
import discord
from datetime import datetime, timedelta
from discord.utils import get
from discord.ext import commands, tasks
bot = commands.Bot(command_prefix = "//", description = "Bot LDC")

f = open('./joueurs.json', 'r')
joueurs = json.load(f)
f.close()

f = open("./équipes.json", "r")
équipes = json.load(f)
f.close()

scope = [   "https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
creads = ServiceAccountCredentials.from_json_keyfile_name("creads.json", scope)
client = gspread.authorize(creads)
sheet = client.open("Marché").sheet1
#data = sheet.get_all_records()
#pprint(data)
#row = sheet.row_values(3)
#col = sheet.col_values(3)
#cell = sheet.cell(3,4).value
#pprint(cell)

#COMMANDS

# Inscription 

@bot.command()
async def inscription(ctx):
    message = ctx.message
    author = message.author
    channel = message.channel
    await ctx.message.delete()

    #Vérification si l'auteur est déjà inscrit

    role_nouveau = ctx.guild.roles[1]
    role_inscrit = ctx.guild.roles[2]

    for role in author.roles :
        if role == role_inscrit :
            await author.send("⚠️ Tu es déjà inscrit ! ⚠️")
            return
    await author.send("** 🏆 INSCRIPTION LOCKDOWN CUP 🏆 **")                    
    
    #Demande du pseudo
    def check_message(message) :
        return message.author == ctx.message.author
    pseudo_correct = False

    while pseudo_correct == False :

        await author.send("❓ Quel est ton pseudo in-game ? ❓")
        try :
            message_pseudo = await bot.wait_for("message", timeout = 40, check = check_message)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return

        pseudo = message_pseudo.content

        if pseudo != "" :
            pseudo_correct = True
        else :
            await author.send("⚠️ Ton pseudo est incorrect ! ⚠️")

    #Demande du btag

    btag_correct = False

    while btag_correct == False :

        await author.send("❓ Quel est ton battletag ? ❓")
        try :
            message_btag = await bot.wait_for("message", timeout = 40, check = check_message)
        
        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return
        
        btag = message_btag.content

        if btag != "" :
            btag_correct = True
        else :
            await author.send("⚠️ Ton battletag est incorrect ! ⚠️")

    #Demande de la côte actuelle

    cote_actuelle_correcte = False

    while cote_actuelle_correcte == False :

        await author.send("❓ Quel est ta côte actuelle **sur ton rôle principal** ? ❓")
        try :
            message_cote_actuelle = await bot.wait_for("message", timeout = 40, check = check_message)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return

        cote_actuelle = int(message_cote_actuelle.content)

        if cote_actuelle >= 1500 and cote_actuelle <= 4700 :
            cote_actuelle_correcte = True
        else :
            await author.send("⚠️ Ta côte actuelle est incorrecte ! ⚠️")

    #Demande du peak de côte

    cote_peak_correcte = False

    while cote_peak_correcte == False :

        await author.send("❓ Quel est ton pic de carrière **tous rôles confondus, toutes saisons confondues, tous comptes confondus** ? ❓")
        try :
            message_cote_peak = await bot.wait_for("message", timeout = 40, check = check_message)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return
        
        cote_peak = int(message_cote_peak.content)

        if cote_peak >= 1500 and cote_peak <= 4700 :
            if cote_peak >= cote_actuelle :
                cote_peak_correcte = True
            else :
                await author.send("⚠️ Ton pic de carrière est inférieur à ta côte actuelle ! ⚠️")
        else :
            await author.send("⚠️ Ton pic de carrière est incorrect ! ⚠️")

    #Demande du rôle

    message_roles = await author.send("❓ Quel est **ton rôle principal** ? *(Tank, Dps, Heal ou Flex)* ❓")
    await message_roles.add_reaction("🛡️")
    await message_roles.add_reaction("⚔️")
    await message_roles.add_reaction("💊")
    await message_roles.add_reaction("♻️")

    def check_reaction(reaction, user) :
        return user == ctx.message.author and message_roles.id == reaction.message.id and (str(reaction.emoji) == "🛡️" or str(reaction.emoji) == "⚔️" or str(reaction.emoji) == "💊" or str(reaction.emoji) == "♻️")

    try :
        reaction, user = await bot.wait_for("reaction_add", timeout = 40, check = check_reaction)

    except :
        await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
        return

    if reaction.emoji == "🛡️" :
        role = 'Tank'
    elif reaction.emoji == "⚔️" :
        role = 'Dps'
    elif reaction.emoji == "💊" :
        role = 'Heal'
    elif reaction.emoji == "♻️" :
        role = 'Flex'

    #Demande des meilleurs picks

    picks_corrects = 0

    while picks_corrects < 3 :

        await author.send("❓ Quels sont tes **3 meilleurs picks** (tous rôles confondus) ? ❓")
        await author.send("```\npick1,pick2,pick3\n```")
        try :
            message_picks = await bot.wait_for("message", timeout = 40, check = check_message)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return

        picks = []
        picks.extend(message_picks.content.split(","))

        for pick in picks :
            if pick != "" :
                picks_corrects += 1
            else :
                await author.send("⚠️ Un de tes picks est incorrect ! ⚠️")
                picks_corrects = 0
    commentaire_correct = False
    while commentaire_correct == False :
        await author.send("❓ Veux-tu ajouter un commentaire ? ❓\n 1- Oui \n2 - Non\n Attention tout commentaire sortant de la charte de réglement sera supprimé et pourra mener à une enquête contre vous")
        try :
            message_commentaire = await bot.wait_for("message", timeout = 60, check = check_message)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return
        choix = int(message_commentaire.content)
        if choix <= 2 and choix >= 1 :
            commentaire_correct = True
        else :
            await author.send("⚠️ Choix incorrecte ! ⚠️")
        if choix == 1:
                commentaire_correct = False
                while commentaire_correct == False:
                    await author.send("Commentaire : ")
                    try :
                        message_commentaire = await bot.wait_for("message", timeout = 60, check = check_message)
                    except:
                        await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
                        return
                    commentaire = message_commentaire.content
                    commentaire_correct = True
        if choix ==2 : 
            commentaire = "/"        
            
    #Obtention du moment d'inscription

    date_inscription = datetime.now().strftime('%d/%m/%Y %H:%M')

    #Calcule du prix du joueur

    prix = round(((abs(2000-cote_actuelle)*0.0005)+1)*((0.7*cote_peak+1.3*cote_actuelle)/2)*15-2)

    #Inscription du joueur dans le fichier de données
    joueurs.append({
        "pseudo" : pseudo,
        "author.id" : author.id,
        "btag" : btag,
        "cote_actuelle" : cote_actuelle,
        "cote_peak" : cote_peak,
        "role" : role,
        "picks" : picks,
        "prix" : prix,
        "date_inscription" : date_inscription,
    })
    f = open('./joueurs.json', 'w')
    json.dump(joueurs, f)
    f.close()
    #Inscription du joueur dans le google sheet
    insertRow = [pseudo, cote_peak, cote_actuelle, btag, role,commentaire,prix]
    sheet.insert_row(insertRow,2)
    #Attribution du rôle

    await author.remove_roles(role_nouveau)
    await author.add_roles(role_inscrit)

    #Confirmation

    await author.send("✅ Vous avez bien été enregistré comme agent libre dans la LockDown Cup ! ✅\nPensez à poser votre candidature en CV dans le channel dédié pour augmenter vos chances de vous faire recruter !")
    

#- modification
@bot.command()
async def modification(ctx):
    f = open('./joueurs.json', 'r')
    joueurs = json.load(f)
    f.close()
    author = ctx.message.author
    await ctx.message.delete()
    
    def check_message(message) :
        return message.author == ctx.message.author

    #Vérification si l'auteur est inscrit

    role_nouveau = ctx.guild.roles[1]

    for role in author.roles :
        if role == role_nouveau :
            await author.send("⚠️ Tu n'es pas encore inscrit ! ⚠️")
            return
    
    joueur_trouve = False

    for joueur in joueurs :
        if author.id == joueur['author.id'] :
            joueur_trouve = True

    if joueur_trouve == False :
        await author.send("⚠️ Erreur : Vous n'êtes pas reconnu dans le fichier de données ! ⚠️")
        print('ERREUR : Index non-trouvé 00010 !')
        return
    
    await author.send("** 🏆 MODIFICATION DES INFORMATIONS PERSONNELLES 🏆 **")
    def check_message(message):
        return message.author == ctx.message.author
    modifications_terminees = False
    while modifications_terminees == False :

        #Demande des infos à modifier

        choix_valide = False
        while choix_valide == False :

            await author.send(f"```\nVos informations personnelles :\n\n1 - Pseudo : {joueur['pseudo']}\n2 - BattleTag : {joueur['btag']}\n3 - Côtes : {joueur['cote_peak']} | {joueur['cote_actuelle']}\n4 - Rôle : {joueur['role']}\n5 - Picks : {joueur['picks'][0]} | {joueur['picks'][1]} | {joueur['picks'][2]}\n6 - Annuler\n```")
            await author.send("❓ Quelles informations souhaitez-vous modifier ? (entrez **le numéro de la ligne**) ❓")
            
            try :
                choix_message = await bot.wait_for("message", timeout = 40, check = check_message)

            except :
                await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                return

            choix = int(choix_message.content)
            if choix <= 6 and choix >= 1 :
                choix_valide = True
            else :
                await author.send("⚠️ Votre choix n'est pas correct ! ⚠️")

        #Modifier Pseudo

        if choix == 1 :

            print("choix1")

            pseudo_correct = False

            while pseudo_correct == False :

                await author.send("❓ Quel est ton pseudo in-game ? ❓")
                try :
                    message_pseudo = await bot.wait_for("message", timeout = 40, check = check_message)

                except :
                    await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                    return

                pseudo = message_pseudo.content

                if pseudo != "" :
                    pseudo_correct = True
                else :
                    await author.send("⚠️ Ton pseudo est incorrect ! ⚠️")
            
            #Inscription de la variable dans l'API

            f = open('joueurs.json', 'r')
            ldc_api = json.load(f)
            f.close()

            joueur["pseudo"] = pseudo
            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

        #Modifier Btag

        if choix == 2 :

            btag_correct = False

            while btag_correct == False :

                await author.send("❓ Quel est ton battletag ? ❓")
                try :
                    message_btag = await bot.wait_for("message", timeout = 40, check = check_message)
                
                except :
                    await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                    return
                
                btag = message_btag.content

                if btag != "" :
                    btag_correct = True
                else :
                    await author.send("⚠️ Ton battletag est incorrect ! ⚠️")
            
            #Inscription de la variable dans l'API

            f = open('joueurs.json', 'r')
            ldc_api = json.load(f)
            f.close()

            joueur["btag"] = btag
            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

        #Modifier Côtes

        if choix == 3 :

            #Demande de la côte actuelle

            cote_actuelle_correcte = False

            while cote_actuelle_correcte == False :

                await author.send("❓ Quel est ta côte actuelle **sur ton rôle principal** ? ❓")
                try :
                    message_cote_actuelle = await bot.wait_for("message", timeout = 40, check = check_message)

                except :
                    await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                    return

                cote_actuelle = int(message_cote_actuelle.content)

                if cote_actuelle >= 1500 and cote_actuelle <= 4700 :
                    cote_actuelle_correcte = True
                else :
                    await author.send("⚠️ Ta côte actuelle est incorrecte ! ⚠️")

            #Demande du peak de côte

            cote_peak_correcte = False

            while cote_peak_correcte == False :

                await author.send("❓ Quel est ton pic de carrière **tous rôles confondus, toutes saisons confondues, tous comptes confondus** ? ❓")
                try :
                    message_cote_peak = await bot.wait_for("message", timeout = 40, check = check_message)

                except :
                    await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                    return
                
                cote_peak = int(message_cote_peak.content)

                if cote_peak >= 1500 and cote_peak <= 4700 :
                    if cote_peak >= cote_actuelle :
                        cote_peak_correcte = True
                    else :
                        await author.send("⚠️ Ton pic de carrière est inférieur à ta côte actuelle ! ⚠️")
                else :
                    await author.send("⚠️ Ton pic de carrière est incorrect ! ⚠️")
            
            #Inscription de la variable dans l'API

            f = open('joueurs.json', 'r')
            ldc_api = json.load(f)
            f.close()

            joueur["cote_actuelle"] = cote_actuelle
            joueur["cote_peak"] = cote_peak
            joueur["prix"] = round(((abs(2000-cote_actuelle)*0.0005)+1)*((0.7*cote_peak+1.3*cote_actuelle)/2)*15-2) 
            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

        #Modifier Rôle

        if choix == 4 :

            #Demande du rôle

            message_roles = await author.send("❓ Quel est **ton rôle principal** ? *(Tank, Dps, Heal ou Flex)* ❓")
            await message_roles.add_reaction("🛡️")
            await message_roles.add_reaction("⚔️")
            await message_roles.add_reaction("💊")
            await message_roles.add_reaction("♻️")

            def check_reaction(reaction, user) :
                return user == ctx.message.author and message_roles.id == reaction.message.id and (str(reaction.emoji) == "🛡️" or str(reaction.emoji) == "⚔️" or str(reaction.emoji) == "💊" or str(reaction.emoji) == "♻️")

            try :
                reaction, user = await bot.wait_for("reaction_add", timeout = 40, check = check_reaction)

            except :
                await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                return

            if reaction.emoji == "🛡️" :
                role = 'Tank'
            elif reaction.emoji == "⚔️" :
                role = 'Dps'
            elif reaction.emoji == "💊" :
                role = 'Heal'
            elif reaction.emoji == "♻️" :
                role = 'Flex'
            
            #Inscription de la variable dans l'API

            f = open('joueurs.json', 'r')
            ldc_api = json.load(f)
            f.close()

            joueur["role"] = role
            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

        #Modifier Picks

        if choix == 5 :

            #Demande des meilleurs picks

            picks_corrects = 0

            while picks_corrects < 3 :

                await author.send("❓ Quels sont tes **3 meilleurs picks** (tous rôles confondus) ? ❓")
                await author.send("```\npick1,pick2,pick3\n```")
                try :
                    message_picks = await bot.wait_for("message", timeout = 40, check = check_message)

                except :
                    await author.send("⌛ Vous avez mis trop de temps a répondre, la procédure s'est annulée ! ⌛")
                    return

                picks = []
                picks.extend(message_picks.content.split(","))

                for pick in picks :
                    if pick != "" :
                        picks_corrects += 1
                    else :
                        await author.send("⚠️ Un de tes picks est incorrect ! ⚠️")
                        picks_corrects = 0

            #Inscription de la variable dans l'API

            f = open('joueurs.json', 'r')
            ldc_api = json.load(f)
            f.close()

            print(joueur['picks'])

            i = 0
            while i < 3 :
                joueur['picks'].pop(0)
                i += 1

            print(joueur['picks'])

            for pick in picks :
                joueur['picks'].append(pick)

            print(joueur['picks'])

            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

        #Quitter

        if choix == 6 :
            return
        
        #Update

        f = open('./joueurs.json', 'r')
        joueurs = json.load(f)
        f.close()

        await author.send(f"```\nVos informations personnelles :\n\n1 - Pseudo : {joueur['pseudo']}\n2 - BattleTag : {joueur['btag']}\n3 - Côtes : {joueur['cote_peak']} | {joueur['cote_actuelle']}\n4 - Rôle : {joueur['role']}\n5 - Picks : {joueur['picks'][0]} | {joueur['picks'][1]} | {joueur['picks'][2]}\n6 - Annuler\n```")
        message_confirm = await author.send("❓ Les modifications sont-elles correctes ? ❓")

        await message_confirm.add_reaction("✔️")
        await message_confirm.add_reaction("❌")

        def check_reaction_confirm(reaction, user) :
            return user == ctx.message.author and message_confirm.id == reaction.message.id and (str(reaction.emoji) == "✔️" or str(reaction.emoji) == "❌")

        try :
            reaction, user = await bot.wait_for("reaction_add", timeout = 40, check = check_reaction_confirm)

        except :
            await author.send("⌛ Vous avez mis trop de temps a répondre, l'inscription s'est annulée ! ⌛")
            return

        if reaction.emoji == "✔️" :
            await author.send("✅ Vos modifications ont bien été prises en compte ! ✅")

            #Inscription de la valeur dans l'API

            f = open('./joueurs.json', 'r')
            joueurs = json.load(f)
            f.close()


            derniere_modification = datetime.now().strftime('%d/%m/%Y %H:%M')
            joueur['derniere_modification'] = derniere_modification

            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

            modifications_terminees = True

        elif reaction.emoji == "❌" :
            pass

#- desinscription
@bot.command()
async def resignation(ctx, joueurUser : discord.User) :
    author = ctx.message.author
    await ctx.message.delete()
    f = open('./joueurs.json', 'r')
    joueurs = json.load(f)
    f.close()

    joueur = ctx.guild.get_member(joueurUser.id)

    #Verification des droits

    a_permissions = False
    is_author = False
    est_nouveau = False

    role_moderateur = ctx.guild.roles[4]
    role_inscrit = ctx.guild.roles[2]
    role_nouveau = ctx.guild.roles[1]

    if joueur == author :
        a_permissions = True
        is_author = True
    for role in author.roles :
        if role == role_moderateur :
            a_permissions = True
        if role == role_nouveau :
            est_nouveau = True

    if est_nouveau == True :
        await author.send("⚠️ Tu n'es pas inscrit à la LDC ! ⚠️")
        return
    if a_permissions == False :
        await author.send("⚠️ Tu n'as pas les droits pour lancer cette commande ! ⚠️")
        return

    #Suppression de la liste des joueurs

    for joueur in joueurs :
        if author.id == joueur["author.id"]:
            del joueur["pseudo"]
            del joueur["author.id"]
            del joueur["btag"]
            del joueur["cote_actuelle"]
            del joueur["cote_peak"]
            del joueur["role"]
            del joueur["picks"]
            del joueur["date_inscription"]
            f = open('joueurs.json', 'w')
            json.dump(joueurs, f)
            f.close()

    #Rétrogradation des rôles

    for role in author.roles :
        await author.remove_roles(role_inscrit)

    await author.add_roles(role_nouveau)

    #Confirmation

    if is_author == True :
        await author.send(f"✅ Vous vous êtes bien désinscrit(e) ! ✅")
    else :
        await author.send(f"✅ **{author.name}** a bien été désinscrit(e) ! ✅")

#- création d équipe dans la ligue

#- supprimer une équipe dans la ligue

#- signer_contrat

#- annuler_contrat

#- info joueur

@bot.command()
async def info(ctx, joueurUser : discord.User) :
    message = ctx.message
    author = message.author
    channel = message.channel
    await ctx.message.delete()
    f = open('./joueurs.json', 'r')
    joueurs = json.load(f)
    f.close()
    joueur_trouvé = False
    for joueur in joueurs :
        if joueur['author.id'] == joueurUser.id :
            joueur_trouvé = True
            joueur_color = "0xff7b00"
            joueur_logo = "../cup_logo5.png"
    if joueur_trouvé == False :   
        await author.send("⚠️ Le joueur recherché n'est pas inscrit ! ⚠️")
        return

    embed = discord.Embed(title = f"__***Infos : {joueur['pseudo']}***__", color=int(joueur_color, base = 16))
    embed.add_field(name = "Pseudo", value = joueur['pseudo'], inline = True)
    embed.add_field(name = "Pic de côte", value = joueur['cote_peak'], inline = True)
    embed.add_field(name = "Valeur", value = (f"{joueur['prix']}$"), inline = True)
    embed.add_field(name = "BTag", value = joueur['btag'], inline = True)
    embed.add_field(name = "Côte actuelle", value = joueur['cote_actuelle'], inline = True)
    embed.add_field(name = "Rôle", value = joueur['role'], inline = True)
    embed.add_field(name = "Picks", value = (f"{joueur['picks'][0]} / {joueur['picks'][1]} / {joueur['picks'][2]}"), inline = True)
    embed.add_field(name = "Date d'inscription", value = joueur['date_inscription'], inline = True)
    await message.author.send(embed=embed)
    return

#- info équipe 

#- info marché

#- set manager

#- unset manager

bot.run("ODUwOTM1MzczMjQ0NTMwNzQ4.YLw9Ug.gMH_EVWEQW--VSHmaBC7hm_EsAY")
