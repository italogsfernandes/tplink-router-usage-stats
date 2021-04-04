import app_van
import app_jair


def main():
    print("#"*80)
    print("# Van")
    print("#"*80)
    try:
        app_van.main(show_result=False)
    except Exception as exc:
        print(exc)

    print("#"*80)
    print("# Jair")
    print("#"*80)
    try:
        app_jair.main(show_result=True)
    except Exception as exc:
        print(exc)

if __name__ == '__main__':
    main()