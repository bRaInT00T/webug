# webug

Clean data by transforming raw files into proper format and JSON data types given in line data types.

| Variable | Type                 |
| -------- | -------------------- |
| S        | String               |
| N        | Numeric [int, float] |
| BOOL     | Boolean              |
| L        | List                 |
| M        | Map                  |

## Requirements

- Python 3 (3.12 used here)
- Execute permissions on `main.py`
- Input data file located in `./data/input.json`

## Usage

### Example Raw Input Data

#### ./data/input.json

```json
{
  "Name": {"S": " John Doe "},
  "Age": {"N": " 030 "},
  "Active": {"BOOL": " true "},
  "SignUpDate": {"S": "2023-07-29T12:34:56Z"},
  "Tags": {"L": [{"S": "tag1"}, {"S": "tag2"}, {"S": ""}]},
  "Attributes": {"M": {"key1": {"S": "value1"}, "key2": {"N": "002"}}}
}
```

### Execution

#### Print to terminal (minimum requirement)

```bash
python main.py -i ./data/input.json
```

#### Output to file (also prints to terminal)

```bash
python main.py -i ./data/input.json -o ./data/output.json
```

## Logging

Logs are printed to the console and written and retained to log files in `./log/webug_YYYmmdd_HHMMSS.log`

\**Logs can be consolidated by Hour, day, month, year, filename by modifying the creation of the logfile name*

### Examples

#### Full Data/Time

```py
current_dt = datetime.now().strftime('%Y%m%d_%H%M%S')
logging.basicConfig(filename=f'{parent_dir}_{current_dt}.log' ,level=logging.INFO)
```

`./log/webug_20240729_114821.log`

#### Date

```py
current_dt = datetime.now().strftime('%Y%m%d')
logging.basicConfig(filename=f'{parent_dir}_{current_dt}.log' ,level=logging.INFO)
```

Output: `./log/webug_20240729.log`

#### Year

```py
current_dt = datetime.now().strftime('%Y')
logging.basicConfig(filename=f'{parent_dir}_{current_dt}.log' ,level=logging.INFO)
```

Output: `./log/webug_2024.log`

#### File Name

```py
logging.basicConfig(filename=f'{parent_dir}.log' ,level=logging.INFO)
```

Output: `./log/webug.log`

## Notes

Does not account for any other data inconsistencies
