from argparse import ArgumentParser
from MySerializer.MySerializer import MySerializer

def main():
    try:
        parse = ArgumentParser()
        parse.add_argument('file_from',type=str, help='file from which you load data')    
        parse.add_argument('file_to',type=str, help='file to which you save serialized data')
        parse.add_argument('format_from',type=str, help='format from which you deserialize data, can be any of json/xml')
        parse.add_argument('format_to',type=str, help='format to which you serialize data, can be any of json/xml')

        args =  parse.parse_args()

        if args.file_from == args.file_to:
            print("File from and file to are the same. Please check your data and try again")
            exit()

        if args.format_from == args.format_to:
            print("Format from and format to are the same. Please check your data and try again")
            exit()

        from_serializer = MySerializer.createSerializer(args.format_from)
        to_serializer = MySerializer.createSerializer(args.format_to)

        with open(args.file_from) as file:
            obj = from_serializer.load(file)
            with open(args.file_to, "w") as output_file:
                to_serializer.dump(obj, output_file)
    except Exception as e:
        print(e)