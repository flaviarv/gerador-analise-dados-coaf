"""
Gerador da dimensão dim_tempo em modelo Kimball Star Schema.
Gera atributos de tempo a partir das datas das transações.
"""
import pandas as pd

DIAS_SEMANA_PT = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def generate_dim_tempo(datas_unicas: list[str]) -> pd.DataFrame:
    """Gera tabela dimensional de tempo a partir de lista de datas YYYY-MM-DD."""
    records = []
    sorted_dates = sorted(list(set(datas_unicas)))

    for dt_str in sorted_dates:
        dt = pd.to_datetime(dt_str)
        id_tempo = int(dt.strftime("%Y%m%d"))
        mes = dt.month
        trimestre = (mes - 1) // 3 + 1
        semestre = 1 if mes <= 6 else 2
        dia_semana_idx = dt.weekday()
        eh_fim_de_semana = dia_semana_idx in (5, 6)

        records.append({
            "id_tempo": id_tempo,
            "data": dt_str,
            "ano": dt.year,
            "mes": mes,
            "nome_mes": MESES_PT[mes],
            "dia": dt.day,
            "dia_semana": DIAS_SEMANA_PT[dia_semana_idx],
            "dia_semana_numero": dia_semana_idx + 1,
            "trimestre": f"T{trimestre}",
            "semestre": f"S{semestre}",
            "ano_mes": dt.strftime("%Y-%m"),
            "eh_fim_de_semana": eh_fim_de_semana
        })

    return pd.DataFrame(records)