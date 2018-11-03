import boto3
import lxml.etree as ET
import urllib
import os.path
import xmltodict as xd
import argparse

def config_dict():
    # Filename options for conversion
    if not os.path.isfile('customer-gateway-config-formats.xml'):
        xml_file = urllib.request.URLopener()
        xml_file.retrieve("http://ec2-downloads.s3.amazonaws.com/2009-07-15/customer-gateway-config-formats.xml", "customer-gateway-config-formats.xml")

    with open('customer-gateway-config-formats.xml','r') as f:
        return xd.parse(f.read())


def version(args):
    print('aws-vpn-config 0.1.0')


def listConfigOutputFormats(args):
    from prettytable import PrettyTable

    cf = config_dict()
    
    table = PrettyTable()

    # Header
    table.field_names = ['index', 'Vendor', 'Platform', 'Software', 'Filename']
    
    for index, item in enumerate(cf['CustomerGatewayConfigFormats']['Format']):
        table.add_row([index, item['Vendor'], item['Platform'], item['Software'], item['Filename']])
    print(table)


def download(args):
    converter_id = int(args.converter_id) # 10
    vpn_id = args.vpn_id #'vpn-08cad142f9189e87d'
    cf = config_dict()

    #print(converter_id, vpn_id)
    #print(cf)

    client = boto3.client('ec2') #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html

    # VPN Config as XML
    response = client.describe_vpn_connections(
        VpnConnectionIds=[
            vpn_id,
        ],
        DryRun=False
    )

    with open(f'{vpn_id}.xml', 'w') as fs:
        fs.write(response['VpnConnections'][0]['CustomerGatewayConfiguration'])

    # Import XSLT from http://ec2-downloads.s3.amazonaws.com/2009-07-15/customer-gateway-config-formats.xml
    filename_parser = cf['CustomerGatewayConfigFormats']['Format'][converter_id]['Filename']
    if not os.path.isfile(filename_parser):
        xlst_file = urllib.request.URLopener()
        xlst_file.retrieve(f"http://ec2-downloads.s3.amazonaws.com/2009-07-15/{filename_parser}", filename_parser)

    # Parse Config as FortiOS config file
    dom = ET.parse(f'{vpn_id}.xml')
    xslt = ET.parse(filename_parser)
    transform = ET.XSLT(xslt)
    config = transform(dom)

    with open (f'{vpn_id}.txt', 'w') as fs:
        fs.write(str(config))

    print(f'Files created: {filename_parser}, {vpn_id}.xml and {vpn_id}.txt' )

def main():
    parser = argparse.ArgumentParser(description='Download VPN Configurations and convert to vendor config (As same as Download Configuration from AWS console).\n Examples:  $ aws-vpn-config download --vpn-id vpn-08cad142f9189e87d -c 10. $ aws-vpn-config list')
    subparsers = parser.add_subparsers(dest='cmd', help='Commands')

    parser_list = subparsers.add_parser('list', help='List all converters')
    parser_list.set_defaults(func=listConfigOutputFormats)

    parser_version = subparsers.add_parser('version', help='Prints the version')
    parser_version.set_defaults(func=version)

    parser_download = subparsers.add_parser('download', help='Download config and converter')
    parser_download.add_argument('-c', '--converter-id', action='store', dest='converter_id', help='ID of config converter. Use --list to see all options')
    parser_download.add_argument('-v', '--vpn-id', action='store', dest='vpn_id', help='AWS VPN ID')
    parser_download.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()