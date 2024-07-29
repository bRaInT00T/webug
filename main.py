from datetime import datetime
import getopt
import json
import logging
import sys
import time
import os

logger = logging.getLogger(__name__)

def init_logging():
    if not os.path.exists('log'):
        os.makedirs('log')
    parent_dir = f'./log/{os.getcwd().rsplit("/")[-1]}'
    current_dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(filename=f'{parent_dir}_{current_dt}.log', level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def transform_value(value: dict) -> any:
    """
    Transforms a value based on its type.

    Args:
        value: The value to be transformed.

    Returns:
        The transformed value.

    Raises:
        None.
    """
    if 'S' in value: # String
        val = value['S'].strip()
        if val == '':
            return None
        try:
            # Parse RFC3339 datetime
            dt = datetime.fromisoformat(val.replace('Z', '+00:00'))
            return int(dt.timestamp())
        except ValueError:
            return val
    elif 'N' in value: # Numeric
        # Strip surrounding whitespace and leading zeros
        val = value['N'].strip().lstrip('0') or '0'
        try:
            # Return int if it is a non floating point number, else return float
            return int(val) if '.' not in val else float(val)
        except ValueError:
            return None
    elif 'BOOL' in value: # Boolean
        val = value['BOOL'].strip().lower()
        if val in {'1', 't', 'true'}:
            return True
        elif val in {'0', 'f', 'false'}:
            return False
        else:
            return None
    elif 'NULL' in value: # Null
        val = value['NULL'].strip().lower()
        if val in {'1', 't', 'true'}:
            return 'null'
        elif val in {'0', 'f', 'false'}:
            return None
        else:
            return None
    elif 'L' in value: # List
        if isinstance(value['L'], list):
            transformed_list = [transform_value(v) for v in value['L'] if transform_value(v) is not None]
            return transformed_list if transformed_list else None
        else:
            return None
    elif 'M' in value: # Map
        if isinstance(value['M'], dict):
            transformed_map = {k.strip(): transform_value(v) for k, v in value['M'].items() if k.strip() and transform_value(v) is not None}
            return transformed_map if transformed_map else None
        else:
            return None
    else:
        return None

def transform_json(input_json: dict):
    """
    Transforms a JSON object by stripping whitespace from keys and applying a transformation function to the values.

    Args:
        input_json (dict): The input JSON object to be transformed.

    Returns:
        list: A list containing the transformed JSON object.

    """
    transformed = {k.strip(): transform_value(v) for k, v in input_json.items() if k.strip() and transform_value(v) is not None}
    return [transformed]

def read(input: str):
    """
    Reads a JSON file and returns its contents as a Python object.

    Args:
        input (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file is not a valid JSON file.
    """
    with open(input) as f:
        data = json.load(f)
    return data


def write(newData, output):
    """
    Write the given data to a JSON file.

    Args:
        newData (dict): The data to be written to the file.
        output (str): The path of the output file.

    Returns:
        None
    """
    with open(output, 'w') as f:
        json.dump(newData, f, indent=2, sort_keys=True)
        

def log(message: str, level: str = 'info'):
    """
    Logs a message to the console.

    Args:
        message (str): The message to be logged.
        level (str): The logging level.

    Returns:
        None
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'{timestamp}: {message}'
    
    if level == 'info':
        logger.info(msg)
    elif level == 'warning':
        logger.warning(msg)
    elif level == 'error':
        logger.error(msg)
    elif level == 'critical':
        logger.critical(msg)
    else:
        logger.info(msg)


def main(argv):
    """
    This is the main function that performs the main logic of the program.
    It reads input from a JSON file, transforms the data, and prints the transformed JSON.
    If specified, it also writes the transformed JSON to an output file.
    """
    start = time.time()
    inputfile = ''
    outputfile = ''
    
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        log('Invalid arguments. Usage: main.py -i <inputfile> -o <outputfile>', 'error')
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
            log(f'Input file is "{inputfile}"')
        elif opt in ("-o", "--output"):
            outputfile = arg
            log(f'Output file is "{outputfile}"')
    
    if not inputfile:
        log('Input file not specified.', 'error')
        sys.exit(2)
        
    input = read(inputfile)
    transformed_json = transform_json(input)
    end = time.time()

    if outputfile:
        log('Writing to output file...')
        write(transformed_json, outputfile)
        
    log('Printing transformed JSON...')
    print(json.dumps(transformed_json, indent=2, sort_keys=True))
    log(f"Processing time: {end - start} seconds")
    
    
if __name__ == "__main__":
    init_logging()
    main(sys.argv[1:])
