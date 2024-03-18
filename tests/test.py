from main import Container, TVS, replace_tvs

cont_1 = Container(1)
cont_1.tvs_lst.append(TVS("11", 1) )
cont_1.tvs_lst.append(TVS("21", 1))

cont_2 = Container(2)
cont_2.tvs_lst.append(TVS("12", 2))
cont_2.tvs_lst.append(TVS("22", 2))

if __name__ == "__main__":

    replace_tvs(cont_1, cont_2, 0, 1)
    replace_tvs(cont_1, cont_2, 0, 1)

    pass