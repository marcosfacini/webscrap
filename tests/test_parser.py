import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraper.parser import parse_process_list, parse_process_detail


SAMPLE_LIST_HTML = """
<table width="99%" class="infraTable" summary="" fonte="Con:MG/Main:MG">
<caption class="infraCaption">Lista de Partes (7 registros):</caption><tbody><tr><th class="infraTh">Nome da Parte</th>
<th class="infraTh">CPF / CNPJ</th>
</tr>
<tr class="infraTrClara"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11744055603505111117567056790">HELDER RICARDO DE JESUS NASCIMENTO</a></td><td valign="top" align="left">100.**********</td></tr><tr class="infraTrEscura"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11752008113257867781416124661">LUIZ RICARDO TORRES SILVA DE JESUS</a></td><td valign="top" align="left">015.**********</td></tr><tr class="infraTrClara"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11760495569568630981358875068">RICARDO CONCEICAO DE JESUS</a></td><td valign="top" align="left">010.**********</td></tr><tr class="infraTrEscura"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11761240792622823299510055361">RICARDO DE JESUS</a></td><td valign="top" align="left">065.**********</td></tr><tr class="infraTrClara"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11760985869030365882900484794">RICARDO DE JESUS ALVES</a></td><td valign="top" align="left">635.**********</td></tr><tr class="infraTrEscura"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11757097637529044395256127064">RICARDO JESUS BECALLI</a></td><td valign="top" align="left">680.**********</td></tr><tr class="infraTrClara"><td valign="top" align="left"><a href="externo_controlador.php?acao=processo_consulta_nome_parte_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica&amp;id_pessoa=11756732857334787676791366772">RICARDO URIAS DE JESUS</a></td><td valign="top" align="left">016.**********</td></tr></tbody></table>
"""


# HTML de exemplo para parse_process_detail, simulando a tabela real
SAMPLE_DETAIL_HTML = """
<table width="99%" class="infraTable" summary="">
<caption class="infraCaption">Lista de Processos (1 registro):</caption><tbody><tr><th class="infraTh" width="15%">Nº Processo</th>
<th class="infraTh" width="25%">Autor</th>
<th class="infraTh">Réu</th>
<th class="infraTh">Assunto</th>
<th class="infraTh">Último Evento</th>
</tr>
<tr class="infraTrClara"><td valign="top" align="left"><a href=\"externo_controlador.php?acao=processo_seleciona_publica&amp;acao_origem=processo_consulta_nome_parte_publica&amp;acao_retorno=processo_consulta_nome_parte_publica&amp;num_processo=10023091920258130145&amp;num_chave=&amp;hash=37b6dcfa2aa5a9f10391cb9aa7ad650e&amp;num_chave_documento=\">1002309-19.2025.8.13.0145</a></td><td valign="top" align="left">ADILSON DA SILVA<br></td><td valign="top" align="left">BANCO C6 S.A.<br></td><td valign="top" align="left"></td><td valign="top" align="left"></td></tr>
</tbody></table>
"""


def test_parse_process_list_ricardo_de_jesus():
    # Testa se encontra o link correto para o nome exato
    name = "RICARDO DE JESUS"
    links = parse_process_list(SAMPLE_LIST_HTML, name)
    assert isinstance(links, list)
    assert len(links) == 1
    assert links[0] == "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_nome_parte_publica&acao_origem=&acao_retorno=processo_consulta_publica&id_pessoa=11761240792622823299510055361"

def test_parse_detail():
    d = parse_process_detail(SAMPLE_DETAIL_HTML)
    assert d["numero_processo"] == "1002309-19.2025.8.13.0145"
    assert d["autor"] == "ADILSON DA SILVA"
    assert d["reu"] == "BANCO C6 S.A."
