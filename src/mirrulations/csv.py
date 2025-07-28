import os
import json
import csv
import click
from tqdm import tqdm


def resolve_output_path(output_option, docket_id):
    import os
    if output_option:
        if os.path.isdir(output_option) or output_option.endswith(os.sep):
            return os.path.join(output_option, f"{docket_id}.csv")
        else:
            return output_option
    else:
        return os.path.join(os.getcwd(), f"{docket_id}.csv")

@click.command("csv")
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, readable=True))
@click.option('-o', '--output', type=click.Path(), default=None, help='Output CSV file path or directory')
@click.option('--dryrun', is_flag=True, help='Only report which fields will be included or excluded, do not write CSV')
@click.option('-include', multiple=True, help='Force-include a field that would otherwise be omitted due to constant value')
def main(input_dir, output, dryrun, include):
    """
    Convert a directory of JSON files (all with the same structure) to a CSV file.
    """
    # Extract docketID from the first file
    first_file = next((f for f in os.listdir(input_dir) if f.endswith('.json')), None)
    if not first_file:
        click.echo('No JSON files found in input directory.')
        return
    with open(os.path.join(input_dir, first_file), 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            click.echo(f'Error reading {first_file}: {e}')
            return
        # Verify this is a comment file
        if 'data' not in data or 'attributes' not in data['data'] or 'type' not in data['data'] or data['data']['type'] != 'comments':
            click.echo('Error: Directory does not contain comment data.')
            return
        docket_id = data['data']['attributes']['docketId']
    output_path = resolve_output_path(output, docket_id)
    click.echo(f'Output CSV will be: {output_path}')
    # Step 1: Scan all JSON files to determine field stats
    attribute_fields = set()
    null_fields = set()
    constant_fields = dict()  # field -> value
    variable_fields = set()
    field_values = dict()  # field -> set of seen values
    total_files = 0
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    if not input_files:
        click.echo('No JSON files found in input directory.')
        return
    for filename in tqdm(input_files, desc='Scanning JSON files'):
        total_files += 1
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                click.echo(f'Error reading {filename}: {e}')
                continue
            attributes = data['data'].get('attributes', {})
            for field, value in attributes.items():
                attribute_fields.add(field)
                if field not in field_values:
                    field_values[field] = set()
                field_values[field].add(json.dumps(value, sort_keys=True))
    # Analyze fields
    for field in attribute_fields:
        values = field_values[field]
        if all(json.loads(v) is None for v in values):
            null_fields.add(field)
        elif len(values) == 1:
            constant_fields[field] = json.loads(next(iter(values)))
        else:
            variable_fields.add(field)
    # Apply -include override
    include_set = set(include)
    for field in include_set:
        if field in constant_fields:
            variable_fields.add(field)
            constant_fields.pop(field)
    # Step 2: Report field analysis
    click.echo('\n--- Field Analysis Report ---')
    click.echo('Fields to be included:')
    for field in sorted(["id", "api_url"] + list(variable_fields)):
        click.echo(f'  {field}')
    click.echo('Fields excluded because all values were null:')
    for field in sorted(null_fields):
        click.echo(f'  {field}')
    click.echo('Fields excluded because all values were the same:')
    for field, value in constant_fields.items():
        click.echo(f'  {field}: {repr(value)}')

    if dryrun:
        return
    # Step 3: Write CSV
    csv_fields = ["id", "api_url"] + sorted(variable_fields)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        for filename in tqdm(input_files, desc='Writing CSV'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    click.echo(f'Error reading {filename}: {e}')
                    continue
                row = {}
                row['id'] = data['data'].get('id', '')
                row['api_url'] = data['data'].get('links', {}).get('self', '')
                attributes = data['data'].get('attributes', {})
                for field in variable_fields:
                    row[field] = attributes.get(field, '')
                writer.writerow(row)

if __name__ == "__main__":
    main()
