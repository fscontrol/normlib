from dataclasses import dataclass

@dataclass
class ROParameters:
    """Входные параметры для расчета"""
    p_feed: float  # Давление подачи
    c_feed: float # Проводимость подачи
    q_feed: float # Поток подачи
    p_conc: float # Давление концентрата
    p_perm: float
    q_perm: float
    c_perm: float
    temp: float # Температура
    square: float # Площадь мембраны
