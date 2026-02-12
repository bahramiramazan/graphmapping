from sources.set_config import page_1, page_2, page_3, page_4
from sources.load_data import load_config
import yaml


def run_page(page_n, info=None):
    if page_n == 1:
        return page_1.page_1(info)
    if page_n == 2:
        return page_2.page_2(info)
    if page_n == 3:
        return page_3.page_3(info)
    if page_n == 4:
        return page_4.page_4(info)
    else:
        raise Exception("Wrong page number")


def create_new_config(info, config_name="config.yaml"):
    f = open(config_name, 'w+')
    yaml.safe_dump(info, f, allow_unicode=True)


if __name__ == "__main__":
    actual_page = 1
    try:
        information = load_config("config.yaml")
    except:
        information = {1: None, 2: None, 3: None, 4: None}
    while True:
        try:
            information[actual_page]
        except:
            information[actual_page] = None
        page_result = run_page(actual_page, information[actual_page])
        if page_result == "close":
            exit()
        elif page_result == "go_back":
            actual_page -= 1
        elif page_result is None:
            exit()
        elif actual_page == 4:
            information[actual_page] = page_result
            break
        elif page_result is not None:
            information[actual_page] = page_result
            actual_page += 1
        else:
            exit()

    old_config = load_config("config.yaml")
    create_new_config(old_config, "config_last_version.yaml")
    create_new_config(information, "config.yaml")
