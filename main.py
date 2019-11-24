import os
import argparse
import multiprocessing as mp
from pubMed_crawler import *

PROCESSES = 10


def parse_args():
    # parsing arguments from shell
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", type=str, help="Specify your search keyword")
    parser.add_argument("save_path", type=str, help="Specify where you want to save data")
    args = parser.parse_args()

    # create a valid file path for data ahead
    while not os.path.isdir(args.save_path):
        args.save_path = input("%s is not a valid file path, please retry: " % args.save_path)

    save_path = args.save_path.rstrip('\\').rstrip('/')
    path = save_path + '/pubMed_data_%s.xlsx' % args.keyword.replace(" ", '_')
    if os.path.exists(path):
        i = 1
        suffix = '/pubMed_data_%s(%d).xlsx' % (args.keyword.replace(" ", '_'), i)
        while os.path.exists(save_path + suffix):
            i += 1

        path = save_path + suffix
    return args.keyword, path


def get_full_search_pages(keyword, per_page=200) -> list:
    get_html_context(URL, "get", params={"term": keyword})

    container = []
    page_count = 1
    i = 1
    print("Preparing search pages...")
    while i <= page_count:
        form = post_form(keyword, i, page_count, per_page)
        html_context = get_html_context(URL, "post", data=form)
        if i == 1:
            page_count = html_context.find("input", attrs={"class": "num"})
            page_count = int(page_count.attrs["last"])

        container.append(html_context)
        i += 1

    return container


def fast_full_search(keyword):
    # multiprocessing part
    pool = mp.Pool(PROCESSES)
    shared_lst = []
    process_pool = []
    functions = (get_date_of_publish, get_title_abstract)
    html_container = get_full_search_pages(keyword)

    for html_context in html_container:
        html_context = str(html_context)
        process_pool.append(pool.apply_async(page_search,
                                             (functions, html_context))
                            )
    print("Tasks load:", len(html_container))
    pool.close()
    pool.join()
    print("Pool joined")
    for p in process_pool:
        shared_lst.append(p.get())

    return concat(shared_lst, axis=0, ignore_index=True)


if __name__ == '__main__':
    keyword, file_path = parse_args()
    result = fast_full_search(keyword)
    result.to_excel(file_path, index=False, sheet_name="data")
    print("Saved file to %s" % file_path)
