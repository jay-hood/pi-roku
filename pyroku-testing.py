from roku import Roku

some_global = True


def Test():
    def __eq__(self):
        return False


class Test2:
    def do_something(self):
        if not some_global:
            print("False")
        else:
            print("True")


def main():
    rokus = Roku.discover(timeout=10)
    for r in rokus:
        print(r.device_info.model_name)
        for app in r.apps:
            print("\t", app.name)


if __name__ == "__main__":
    t = Test2()
    t.do_something()
