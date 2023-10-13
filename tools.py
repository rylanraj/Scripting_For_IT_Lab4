def prompt(message, valid_values, convert=None):
    response = None

    while True:
        response = input(f"\n{message} ")

        if convert:
            try:
                response = convert(response)

            except:
                print(f"Response must be of type {convert}")

        if response in valid_values:
            return response  # return ends execution of a function
        else:
            print(f"Response must be in {valid_values}")