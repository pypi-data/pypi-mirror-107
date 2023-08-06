import os
import click


def replace_illegal(s):
    illegal = ["\\", "/", ":", "*", '"', "<", ">", "|", "?"]
    for c in illegal:
        s = s.replace(c, "")
    return s


def renamer(path, extension, episodes):
    try:
        os.chdir(path)
        path = os.getcwd()
    except OSError:
        print("Path you entered doesn't exist:", path)

    episodes = [replace_illegal(episode) for episode in episodes]

    series_list = [f"{i:0>2}. {episode}" for i, episode in enumerate(episodes, start=1)]
    files_list = [file for file in next(os.walk("."))[2] if file.endswith(extension)]

    if files_list:
        ext_lambda = lambda p: os.path.splitext(p)[1]
        print("All of your file will be renamed the following way:")
        for src, dst in zip(files_list, series_list):
            print(
                os.path.join(path, src),
                "->",
                os.path.join(
                    path, "".join([dst, extension if extension else ext_lambda(src)])
                ),
            )
        if click.confirm("Do you want to continue?"):
            for src, dst in zip(files_list, series_list):
                os.rename(
                    os.path.join(path, src),
                    os.path.join(
                        path,
                        "".join([dst, extension if extension else ext_lambda(src)]),
                    ),
                )
            print("Done!")
        else:
            exit("Aborted")
    else:
        exit(f"Can't find any files in this path: {path}")
