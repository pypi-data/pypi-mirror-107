import os

if __name__ == '__main__':
    print("from docker")
    print(os.environ["POSTGRES_CONN_STR"])