import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Koch Snowflake')
    parser.add_argument('--latest', action='store_true', help='Use the latest version of the snowflake')
    parser.add_argument('--dev-0', action='store_true', help='Use the dev-0 version of the snowflake') 
    parser.add_argument('--dev-1', action='store_true', help='Use the dev-1 version of the snowflake')
    
    if parser.parse_args().latest:
        from src.app import main
    elif parser.parse_args().dev_0:
        from src.desperated.snowflake_turtle_fixed import main
    elif parser.parse_args().dev_1:
        from src.desperated.snowflake_turtle_scalable import main
    else:
        from src.app import main
    main()