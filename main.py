import os
from copy import deepcopy
from typing import Literal

cur_dir = os.getcwd()
tvs_heat_file = os.path.join(cur_dir, "unit_in.txt")
result_file = os.path.join(cur_dir, "result.txt")


class TVS:
    def __init__(self, number: str, heat: float, coordinates: str):
        self.number: str = number
        self.heat = heat
        self.coordinates = coordinates

    def __str__(self):
        return f"{self.number}  {round(self.heat, 4)} {self.coordinates}"


class Container:
    def __init__(self, number, **kwargs):
        self.number = number
        self.cells_num = kwargs["cells_num"] if kwargs.get("cells_num") else 12
        self.heat = 0.0
        self.tvs_lst: list[TVS] = []

    def __str__(self):
        return f"Контейнер № {self.number}; кол-во ТВС: {len(self.tvs_lst)}; средн. тепловыд.:{self.heat}."

    def calculate_heat(self):
        self.heat = sum(tvs.heat for tvs in self.tvs_lst)


def get_aim_heat(mas: list[TVS | Container], mode: Literal["hot", "cold"]):
    if mode == "hot":
        aim_q = max((elm.heat for elm in mas))
    elif mode == "cold":
        aim_q = min(elm.heat for elm in containers_pool)
    else:
        raise KeyError
    aim_index = [elm.heat for elm in mas].index(aim_q)
    if isinstance(mas[0], Container):
        return mas[aim_index]
    elif isinstance(mas[0], TVS):
        return mas.pop(aim_index)


def tvs_pool_handler(input_file):
    pool = []
    with open(input_file, "r") as file:
        lines = file.readlines()
        _containers_count = int(lines[0])
        for line in lines[1:]:
            line_split = line.split()
            pool.append(TVS(line_split[0].strip(), float(line_split[1]), line_split[2]))
    return _containers_count, pool


def result_file_handler(result_file, containers_pool):
    with open(result_file, "w") as file:
        for container in containers_pool:
            file.write(f"Контейнер № {container.number} ({len(container.tvs_lst)} ТВС), тепловыделение: {round(container.heat, 4)}\n")
            for tvs in container.tvs_lst:
                file.write(f"{tvs}\n")
            file.write("\n")


def average_heat_calculation(mas: list[TVS | Container]):
    return sum([elm.heat for elm in mas]) / len(mas)


def disp_calculate(pool, avg_q):
    return sum([(_cont.heat - avg_q)**2 for _cont in pool])


def replace_tvs(cont_1: Container, cont_2: Container, tvs_1_num: int, tvs_2_num: int):
    tvs_1 = cont_1.tvs_lst[tvs_1_num]
    tvs_2 = cont_2.tvs_lst[tvs_2_num]

    cont_1.tvs_lst.remove(tvs_1)
    cont_2.tvs_lst.remove(tvs_2)

    cont_1.tvs_lst.insert(tvs_1_num, tvs_2)
    cont_2.tvs_lst.insert(tvs_2_num, tvs_1)


if __name__ == "__main__":
    containers_count, tvs_pool = tvs_pool_handler(tvs_heat_file)

    containers_pool = [Container(i) for i in range(1, containers_count + 1)]

    while len(tvs_pool) > 0:
        cold_container = get_aim_heat(containers_pool, "cold")
        hot_tvs = get_aim_heat(tvs_pool, "hot")
        cold_container.tvs_lst.append(hot_tvs)
        cold_container.calculate_heat()

    avg_q = average_heat_calculation(containers_pool)
    base_disp = disp_calculate(containers_pool, avg_q)

    exp_containers_pool = deepcopy(containers_pool)
    for cont_1 in exp_containers_pool:
        for cont_2 in exp_containers_pool:
            if cont_1 != cont_2:
                for tvs_1_num in range(0, len(cont_1.tvs_lst)):
                    for tvs_2_num in range(0, len(cont_2.tvs_lst)):
                        replace_tvs(cont_1, cont_2, tvs_1_num, tvs_2_num)
                        cont_1.calculate_heat()
                        cont_2.calculate_heat()
                        exp_avg_q = average_heat_calculation(exp_containers_pool)
                        exp_disp = disp_calculate(exp_containers_pool, exp_avg_q)
                        if exp_disp < base_disp:
                            base_disp = exp_disp
                            containers_pool = exp_containers_pool
                        else:
                            replace_tvs(cont_1, cont_2, tvs_1_num, tvs_2_num)
                            cont_1.calculate_heat()
                            cont_2.calculate_heat()

    hot_cont = get_aim_heat(containers_pool, "hot")
    cold_cont = get_aim_heat(containers_pool, "cold")
    max_delta_q = hot_cont.heat - cold_cont.heat
    av_q = average_heat_calculation(containers_pool)

    delta_q_cold = av_q - cold_cont.heat
    delta_q_hot = hot_cont.heat - av_q
    result_file_handler(result_file, containers_pool)
    input("Done!")