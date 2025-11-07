import click
import logging
from .runner import ScraperRunner
from .exporter import save_json

DEFAULT_NAMES = [
    "ADILSON DA SILVA",
    "JOÂO DA SILVA MORAES",
    "RICARDO DE JESUS",
    "SERGIO FIRMINO DA SILVA",
    "HELENA FARIAS DE LIMA",
    "PAULO SALIM MALUF",
    "PEDRO DE SÁ",
]

@click.command()
@click.option("--names-file", type=click.Path(), help="Arquivo com nomes (uma linha por nome).")
@click.option("--output", default="output/resultados.json", help="Arquivo JSON de saída.")
@click.option("--headless/--no-headless", default=True)
@click.option("--delay", default=1.0, help="Delay entre requisições (segundos).")
@click.option("--base-url", default="https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica")
def main(names_file, output, headless, delay, base_url):
    logging.basicConfig(level=logging.INFO)
    if names_file:
        with open(names_file, "r", encoding="utf-8") as f:
            names = [l.strip() for l in f if l.strip()]
    else:
        names = DEFAULT_NAMES

    runner = ScraperRunner(base_url=base_url, headless=headless, delay_between_requests=delay)
    data = runner.run_for_names(names)
    save_json(data, output)
    click.echo(f"Resultados salvos em {output}")

if __name__ == "__main__":
    main()
