import xml.etree.ElementTree as ET

# Check out the tutorial at:
# https://github.com/av1d/Python_XML_Tutorial/

tree = ET.parse('test.xml')
root = tree.getroot()

rootKey = './/{this:is:the:namespace}'  # Specify namespace as it is in 'xmlns' attribute of <xml> tag

Timestamp    = root.findall(rootKey + 'Timestamp')[0]  # Find the timestamp
ItemArray    = root.findall(rootKey + 'ItemArray')[0]  # Select the 'ItemArray'

for i in range(0, len(ItemArray)):  # iterate through ItemArray to find each Item.

    # the comment indentation below indicates the XML tree structure.

    Item         = ItemArray.findall(    rootKey + 'Item')[i]           # find 'Item' inside 'ItemArray'
    ItemName     = Item.findall(         rootKey + 'ItemName')[0]           # find 'ItemName' inside 'Item'
    SKU          = Item.findall(         rootKey + 'SKU')[0]                # find 'SKU' inside 'Item'
    OptionsArray = Item.findall(         rootKey + 'OptionsArray')[0]       # Select the 'OptionsArray' inside 'Item'
    Option1      = OptionsArray.findall( rootKey + 'Option1')[0]                # Find 'Option1' inside OptionsArray'
    Option2      = OptionsArray.findall( rootKey + 'Option2')[0]                # Find 'Option2' inside OptionsArray'

    print(
            '\n',
            'Timestamp:', Timestamp.text, '\n',
            'Item Name:', ItemName.text,  '\n',
            '      SKU:', SKU.text,       '\n',
            '  Options:', Option1.text,   ',' , Option2.text,
            '\n',
    )


# Expected output:
#
#   Timestamp: 2023-07-25T16:00:36.000Z 
#   Item Name: Magic Gum 
#         SKU: MGK-508 
#     Options: Snozzberry Flavor , Everlasting Gobstopper Flavor
#
#
#   Timestamp: 2023-07-25T16:00:36.000Z 
#   Item Name: Triangular Yoyo 
#         SKU: YO-1337 
#     Options: Glow In The Dark , 80s Neon 
