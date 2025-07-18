import discord
import asyncio
import json
import os
import re
from colorama import Fore, Style, init

init(autoreset=True)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

ascii_art = f"""{Fore.CYAN}{Style.BRIGHT} 

     _    ____  __  __ ___ _   _                              
 █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ████╗ ████║██╔════╝████╗  ██║██║   ██║
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
"""

print(ascii_art)

GUILD_ID = int(input(Fore.CYAN + "Digite o ID do servidor (Guild ID): "))
TOKEN = input(Fore.CYAN + "Digite o token do bot: ")

def print_menu():
    print(ascii_art)

    print(Fore.GREEN + "\n[===============================================]")
    print(Fore.CYAN + "\n[ Canais e Categorias ]")
    print(Fore.MAGENTA + "[01] Apagar todos os canais")
    print(Fore.MAGENTA + "[04] Criar chats")
    print(Fore.MAGENTA + "[14] Criar categorias")
    print(Fore.MAGENTA + "[26] Listar todos os canais e categorias")

    print(Fore.CYAN + "\n[ Cargos ]")
    print(Fore.MAGENTA + "[02] Apagar todos os cargos")
    print(Fore.MAGENTA + "[06] Atribuir cargo a todos")
    print(Fore.MAGENTA + "[07] Remover cargo de todos")
    print(Fore.MAGENTA + "[08] Criar novo cargo")
    print(Fore.MAGENTA + "[15] Listar todos os cargos")
    print(Fore.MAGENTA + "[24] Deletar cargo ou categoria individualmente")
    print(Fore.MAGENTA + "[25] Deletar cargo individualmente")

    print(Fore.CYAN + "\n[ Membros ]")
    print(Fore.MAGENTA + "[03] Banir todos os membros")
    print(Fore.MAGENTA + "[09] Mandar DM a todos os membros")
    print(Fore.MAGENTA + "[12] Listar membros com IDs")
    print(Fore.MAGENTA + "[13] Listar bots do servidor")
    print(Fore.MAGENTA + "[23] Banir membro individualmente")

    print(Fore.CYAN + "\n[ Mensagens e Comunicação ]")
    print(Fore.MAGENTA + "[05] Mandar mensagem nos canais")

    print(Fore.CYAN + "\n[ Configurações do Servidor ]")
    print(Fore.MAGENTA + "[10] Alterar logo do servidor")
    print(Fore.MAGENTA + "[11] Alterar nome do servidor")

    print(Fore.CYAN + "\n[ Backup ]")
    print(Fore.MAGENTA + "[16] Criar um backup")
    print(Fore.MAGENTA + "[17] Ver os backups")
    print(Fore.MAGENTA + "[18] Deletar um backup")
    print(Fore.MAGENTA + "[19] Executar um backup")
    print(Fore.MAGENTA + "[27] Renomear o backup")

    print(Fore.CYAN + "\n[ Webhooks ]")
    print(Fore.MAGENTA + "[20] Listar webhook")
    print(Fore.MAGENTA + "[21] Criar webhook")
    print(Fore.MAGENTA + "[22] Deletar webhook")

    print(Fore.YELLOW + "\n[00] Sair")
    print(Fore.GREEN + "[===============================================]\n")


async def menu_loop(guild):
    while True:
        print_menu()
        escolha = await asyncio.to_thread(input, Fore.RED + "Escolha o método: ")

        if escolha == "1":
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(Fore.YELLOW + f"Canal deletado: {channel.name}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao deletar canal: {e}")

        elif escolha == "2":
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                        print(Fore.YELLOW + f"Cargo deletado: {role.name}")
                    except Exception as e:
                        print(Fore.RED + f"Erro ao deletar cargo: {e}")

        elif escolha == "3":
            for member in guild.members:
                if not member.bot:
                    try:
                        await guild.ban(member, reason="Ban em massa autorizado.")
                        print(Fore.YELLOW + f"{member.name} banido.")
                    except Exception as e:
                        print(Fore.RED + f"Erro ao banir {member.name}: {e}")

        elif escolha == "4":
            quantidade = int(await asyncio.to_thread(input, "Quantos canais deseja criar? "))
            nome = await asyncio.to_thread(input, "Nome base dos canais: ")
            for i in range(quantidade):
                try:
                    await guild.create_text_channel(f"{nome}-{i+1}")
                    print(Fore.YELLOW + f"Canal criado: {nome}-{i+1}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao criar canal: {e}")

        elif escolha == "5":
            mensagem = await asyncio.to_thread(input, "Mensagem a ser enviada: ")
            for channel in guild.text_channels:
                try:
                    await channel.send(mensagem)
                    print(Fore.YELLOW + f"Mensagem enviada em: {channel.name}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao enviar mensagem em {channel.name}: {e}")

        elif escolha == "6":
            role_id = int(await asyncio.to_thread(input, "ID do cargo para atribuir: "))
            role = guild.get_role(role_id)
            if role:
                for member in guild.members:
                    try:
                        await member.add_roles(role)
                        print(Fore.GREEN + f"{member.name} recebeu o cargo.")
                    except Exception as e:
                        print(Fore.RED + f"Erro ao atribuir cargo: {e}")
            else:
                print(Fore.RED + "Cargo não encontrado.")

        elif escolha == "7":
            role_id = int(await asyncio.to_thread(input, "ID do cargo para remover: "))
            role = guild.get_role(role_id)
            if role:
                for member in guild.members:
                    try:
                        await member.remove_roles(role)
                        print(Fore.YELLOW + f"{member.name} teve o cargo removido.")
                    except Exception as e:
                        print(Fore.RED + f"Erro ao remover cargo: {e}")
            else:
                print(Fore.RED + "Cargo não encontrado.")

        elif escolha == "8":
            nome = await asyncio.to_thread(input, "Nome do novo cargo: ")
            cor_hex = await asyncio.to_thread(input, "Cor hexadecimal (ex: #ff0000): ")
            admin = await asyncio.to_thread(input, "Permissões administrativas? (y/n): ")

            try:
                cor = discord.Color.default()
                if cor_hex.startswith("#"):
                    cor = discord.Color(int(cor_hex[1:], 16))
                perms = discord.Permissions(administrator=True) if admin.lower() == "y" else discord.Permissions(send_messages=True, read_messages=True)
                novo = await guild.create_role(name=nome, color=cor, permissions=perms)
                print(Fore.YELLOW + f"Cargo criado: {novo.name} (ID: {novo.id})")
            except Exception as e:
                print(Fore.RED + f"Erro ao criar cargo: {e}")

        elif escolha == "9":
            mensagem = await asyncio.to_thread(input, "Mensagem para enviar por DM: ")
            for member in guild.members:
                if not member.bot:
                    try:
                        await member.send(mensagem)
                        print(Fore.LIGHTBLUE_EX + f"DM enviada para: {member.name}")
                    except Exception as e:
                        print(Fore.RED + f"Erro ao enviar para {member.name}: {e}")

        elif escolha == "10":
            caminho = await asyncio.to_thread(input, "Caminho da imagem (ex: logo.png): ")
            try:
                with open(caminho, "rb") as img:
                    await guild.edit(icon=img.read())
                    print(Fore.YELLOW + "Logo alterada com sucesso!")
            except Exception as e:
                print(Fore.RED + f"Erro ao mudar a logo: {e}")

        elif escolha == "11":
            nome = await asyncio.to_thread(input, "Novo nome do servidor: ")
            try:
                await guild.edit(name=nome)
                print(Fore.YELLOW + f"Nome alterado para: {nome}")
            except Exception as e:
                print(Fore.RED + f"Erro ao mudar nome: {e}")

        elif escolha == "12":
            print(Fore.LIGHTGREEN_EX + "\nMembros do servidor:")
            for member in guild.members:
                print(f"{member.name}#{member.discriminator} — ID: {member.id}")

        elif escolha == "13":
            print(Fore.LIGHTCYAN_EX + "\nBots do servidor:")
            for member in guild.members:
                if member.bot:
                    print(f"{member.name}#{member.discriminator} — ID: {member.id}")

        elif escolha == "14":
            qtd = int(await asyncio.to_thread(input, "Quantas categorias criar? "))
            nome = await asyncio.to_thread(input, "Nome base da categoria: ")
            for i in range(qtd):
                try:
                    await guild.create_category(name=f"{nome}-{i+1}")
                    print(Fore.YELLOW + f"Categoria criada: {nome}-{i+1}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao criar categoria: {e}")

        elif escolha == "15":
            print(Fore.LIGHTMAGENTA_EX + "\nCargos disponíveis:")
            for role in guild.roles:
                print(f"{role.name} — ID: {role.id}") 

        elif escolha == "16":
            # Criar um backup básico
            backup = {
                "name": guild.name,
                "roles": [{ "name": r.name, "permissions": r.permissions.value } for r in guild.roles if r.name != "@everyone"],
                "channels": [c.name for c in guild.channels],
            }
            nome_arquivo = f"backup_{guild.id}.json"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(backup, f, indent=4)
            print(Fore.YELLOW + f"Backup salvo como {nome_arquivo}")

        elif escolha == "17":
            arquivos = [f for f in os.listdir() if f.startswith("backup_") and f.endswith(".json")]
            if arquivos:
                print(Fore.LIGHTBLUE_EX + "\nBackups encontrados:")
                for arq in arquivos:
                    print(arq)
            else:
                print(Fore.RED + "Nenhum backup encontrado.")

        elif escolha == "18":
            nome_backup = await asyncio.to_thread(input, "Nome do backup para deletar: ")
            if os.path.exists(nome_backup):
                os.remove(nome_backup)
                print(Fore.YELLOW + f"Backup {nome_backup} deletado.")
            else:
                print(Fore.RED + "Arquivo não encontrado.")

        elif escolha == "19":
            nome_backup = await asyncio.to_thread(input, "Nome do backup para executar: ")
            if os.path.exists(nome_backup):
                with open(nome_backup, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for role in data["roles"]:
                    try:
                        perms = discord.Permissions(role["permissions"])
                        await guild.create_role(name=role["name"], permissions=perms)
                    except Exception as e:
                        print(Fore.RED + f"Erro ao criar cargo: {e}")
                for channel_name in data["channels"]:
                    try:
                        await guild.create_text_channel(channel_name)
                    except Exception as e:
                        print(Fore.RED + f"Erro ao criar canal: {e}")
                print(Fore.GREEN + "Backup executado com sucesso.")
            else:
                print(Fore.RED + "Backup não encontrado.")

        elif escolha == "20":
            print(Fore.LIGHTCYAN_EX + "\nWebhooks encontrados:")
            for channel in guild.text_channels:
                try:
                    webhooks = await channel.webhooks()
                    for webhook in webhooks:
                        print(f"{webhook.name} — URL: {webhook.url}")
                except Exception:
                    continue

        elif escolha == "21":
            canal_id = int(await asyncio.to_thread(input, "ID do canal para criar webhook: "))
            nome = await asyncio.to_thread(input, "Nome do webhook: ")
            canal = guild.get_channel(canal_id)
            if canal:
                try:
                    webhook = await canal.create_webhook(name=nome)
                    print(Fore.YELLOW + f"Webhook criado: {webhook.url}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao criar webhook: {e}")
            else:
                print(Fore.RED + "Canal não encontrado.")

        elif escolha == "22":
            print(Fore.LIGHTRED_EX + "Procurando webhooks para deletar...")
            for channel in guild.text_channels:
                try:
                    webhooks = await channel.webhooks()
                    for webhook in webhooks:
                        await webhook.delete()
                        print(Fore.YELLOW + f"Webhook deletado: {webhook.name}")
                except Exception as e:
                    print(Fore.RED + f"Erro ao deletar webhook: {e}")

        elif escolha == "23":
            membro_id = int(await asyncio.to_thread(input, "ID do membro para banir: "))
            membro = guild.get_member(membro_id)
            if membro:
                try:
                    await guild.ban(membro, reason="Ban manual")
                    print(Fore.YELLOW + f"{membro.name} banido.")
                except Exception as e:
                    print(Fore.RED + f"Erro ao banir membro: {e}")
            else:
                print(Fore.RED + "Membro não encontrado.")

        elif escolha == "24":
            item_id = int(await asyncio.to_thread(input, "ID do cargo/categoria para deletar: "))
            item = discord.utils.get(guild.roles + guild.categories, id=item_id)
            if item:
                try:
                    await item.delete()
                    print(Fore.YELLOW + f"{item.name} deletado.")
                except Exception as e:
                    print(Fore.RED + f"Erro ao deletar: {e}")
            else:
                print(Fore.RED + "Item não encontrado.")

        elif escolha == "25":
            cargo_id = int(await asyncio.to_thread(input, "ID do cargo para deletar: "))
            role = guild.get_role(cargo_id)
            if role:
                try:
                    await role.delete()
                    print(Fore.YELLOW + f"Cargo {role.name} deletado.")
                except Exception as e:
                    print(Fore.RED + f"Erro ao deletar cargo: {e}")
            else:
                print(Fore.RED + "Cargo não encontrado.")

        elif escolha == "26":
            print(Fore.LIGHTCYAN_EX + "\nCategorias e canais do servidor:")
            for category in guild.categories:
                print(f"\n📁 Categoria: {category.name} — ID: {category.id}")
                for channel in category.channels:
                    print(f"   └─ 📄 Canal: {channel.name} — ID: {channel.id}")
            print(Fore.LIGHTCYAN_EX + "\nCanais sem categoria:")
            for channel in guild.channels:
                if not channel.category:
                    print(f"📄 {channel.name} — ID: {channel.id}")

        elif escolha == "27":
            backups = [f for f in os.listdir() if f.endswith(".json")]
            if not backups:
                print(Fore.RED + "Nenhum backup encontrado para renomear.")
            else:
                print(Fore.LIGHTBLUE_EX + "\nBackups disponíveis:")
                for i, arquivo in enumerate(backups, 1):
                    print(f"{i} - {arquivo}")

                escolha_arquivo = await asyncio.to_thread(input, "Digite o número do backup que deseja renomear: ")
                if not escolha_arquivo.isdigit() or not (1 <= int(escolha_arquivo) <= len(backups)):
                    print(Fore.RED + "Escolha inválida.")
                else:
                    arquivo_selecionado = backups[int(escolha_arquivo) - 1]
                    novo_nome = await asyncio.to_thread(input, "Digite o novo nome para o backup (sem extensão): ")
                    novo_nome = novo_nome.strip()
                    if not novo_nome:
                        print(Fore.RED + "Nome vazio. Operação cancelada.")
                    else:
                        novo_nome_arquivo = f"{novo_nome}.json"
                        if os.path.exists(novo_nome_arquivo):
                            print(Fore.RED + "Já existe um arquivo com esse nome.")
                        else:
                            os.rename(arquivo_selecionado, novo_nome_arquivo)
                            print(Fore.YELLOW + f"Backup '{arquivo_selecionado}' renomeado para '{novo_nome_arquivo}'.")

        elif escolha == "28":
            print("Link da nossa org =) : https://discord.gg/uyNFqwdT7W")

        elif escolha == "0":
            print(Fore.RED + "Saindo...")
            await client.close()
            break

        else:
            print(Fore.RED + "Opção inválida.")

        print(Fore.CYAN + "\n>>> Ação concluída. Retornando ao menu...\n")
        await asyncio.sleep(1)


@client.event
async def on_ready():
    print(Fore.GREEN + f"\nBot {client.user} conectado com sucesso!")
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(Fore.RED + "Servidor não encontrado. Verifique se o ID está correto e o bot está no servidor.")
        await client.close()
        return
    print(Fore.GREEN + f"Conectado a: {guild.name} ({guild.id})")
    await menu_loop(guild)


client.run(TOKEN)









