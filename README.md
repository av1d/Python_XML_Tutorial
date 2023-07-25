# Python_XML_Tutorial
A brief tutorial which demonstrates how to process any XML and get up and running quickly.

Or...

**How to Process any XML in Python in 10 minutes**

I made this because I was tired of examples I can't understand
or were overly specific. I am by no means an expert on XML but thought this may be useful to others. Without any BS I will try to break it down for you instantly and hopefully you will be running in no time. This should apply to virtually any XML file you encounter. This will also show you how to grab values from nested tags and tags with the same name under the same child, hopefully with ease. This is what I've found to be the easiest, most readable way. This document also takes into consideration common issues like lack of namespace, double namespaces, nested elements and so on.

Let's go:

We'll use this valid XML snippet throught as illustration.
It has two nested objects in the `<Item>` tag within the `<ItemArray>`. The `<OptionsArray>` for each item has two objects with options for that item.


    <?xml version="1.0" encoding="UTF-8"?>
    <APIResponse xmlns="this:is:the:namespace">
        <Timestamp>2023-07-25T16:00:36.000Z</Timestamp>
    	<ItemArray>
    		<Item>
    			<ItemName>Magic Gum</ItemName>
    			<SKU>MGK-508</SKU>
    			<OptionsArray>
    				<Option1>Snozzberry Flavor</Option1>
    				<Option2>Everlasting Gobstopper Flavor</Option2>
    			</OptionsArray>
    		</Item>
    		<Item>
    			<ItemName>Triangular Yoyo</ItemName>
    			<SKU>YO-1337</SKU>
    			<OptionsArray>
    				<Option1>Glow In The Dark</Option1>
    				<Option2>80s Neon</Option2>
    			</OptionsArray>
    		</Item>
    	</ItemArray>
    </APIResponse>

Always format your XML before trying to break it down, it will be much easier. You can use an 'XML beautifier' online to do this, and you should validate it as well. Most sites do both.

Here's an illustration:

![XML level illustration](https://raw.githubusercontent.com/av1d/Python_XML_Tutorial/main/infographic.png)

Let's quickly break down the structure of the above snippet (skip if you're familiar with XML structure):

We have the XML declaration as the first line: `<?xml version="1.0"  encoding="UTF-8"?>`. 
We have a container as the second line which    contains a namespace: `<APIResponse xmlns="this:is:the:namespace">`.

I like to think of this as a container because it contains ALL of the other elements and itself doesn't have a value. Later on when we reference the namespace (if one exists) to read the document, we do not access this tag directly. Inside this container we have `Timestamp` and `ItemArray` elements.
Inside the `ItemArray` we have additional elements.
Look at the graphic and you can see the indexing numbers. You may notice the indexing starts at index 0 for the first
element (`Timestamp`). The second element (`ItemAray`) is index 1. 
If there is a tag with child tags (example: <`Item><OptionsArray>`, whereas `OptionsArray` is the child of `Item`), the first item inside the parent tag starts at index 0. Formatting your XML before we start will make it easier to read,
we can more easily find nested elements and determine the hierarchy of the XML file.


If you're used to referencing things by index instead of key/tag I would recommend dropping the habit here to create readability unless you can guarantee that the XML will always retain exactly the same format forever no matter what. It is not uncommon for certain fields to only be returned by an API at certain times. Referencing them by tag can prevent reading and coding disasters and it's easier to break it down for readability. This isn't a failsafe because parsing the data by tag can still fail, but it will be much easier (especially if inside of a 'try' clause) to find the error, rather than crossreferencing index numbers to the XML data. 

While this makes the code a tiny bit longer it has better readability. Would you rather be able to decipher the code instantly or spend hours referencing which indexes apply to which tags? It's important to keep in mind that what makes sense now may not in the future when you look back at the code and this practice should help save time if in the future should you need to modify something. Of course, this is my personal opinion, so do as you may, but speaking from experience it is not fun to dissect a bunch of cryptic indexes especially when dealing with massive files with many fields!

Let's say our parsed XML is inside the variable `XMLStructure`. We _could_ access the first option of the first item (`ItemName`) like so: `XMLStructure[1][0][0].text`. This will give us "**Magic Gum**" as the value. Broken down, this translates to: `XMLStructure[ItemArray][Item 0][ItemName]`. To me it's rather confusing to refer to things by index numbers as we cannot see precisely what's going on here, it's basically a blob of text.

As mentioned previously, I personally prefer writing it out the long way:

    ItemArray    = XMLStructure.findall('ItemArray')[0]  # select the ItemArray
    Item         = ItemArray.findall('Item')[0]          # Select Item from ItemArray
    ItemName     = Item.findall('ItemName')[0]           # Select ItemName from Item
    OptionsArray = Item.findall('OptionsArray')          # Select OptionsArray from Item
    
    print(ItemName.text, OptionsArray)

   
If we look at the ElementTree manual:
(https://docs.python.org/2/library/xml.etree.elementtree.html#finding-interesting-elements) under `findall` we will see:

> "Element.findall() finds only elements with a tag which are direct
> children of the current element."

So in the above pseudocode what we're doing is selecting each first element ([0]) then searching within that element for the next first element. Please read the above link to learn how to find other types.

Placing [0] at the end will return the _first_ tag within the previous tag. Omitting the index will return a list. The above example will print the name as a string and _all_ of its options as a Python list. Don't worry, in the final example we'll print the options as strings. The expected output of the above is`: Magic Gum [<Element '{this:is:the:namespace}Option1' at 0x7fe5d9634bd0>, <Element '{this:is:the:namespace}Option2' at 0x7fe5d9634c20>]`
So, as you can see, if you omit the [0] index, it will return a list of child elements.

Example:

    <?xml version="1.0" encoding="UTF-8"?>
    <APIResponse>
    	<test>a</test>
    	<test>b</test>
    </APIResponse>

`test = XMLStructure.findall('test')`  will return a list containing both <test> elements.
`test = XMLStructure.findall('test')[0].text`  will return the text of the first element.
`test = XMLStructure.findall('test')[1].text`  will return the text of the second element.


Finally, here's a working example. First, save the larger XML code from the top of this document into a file '**test.xml**',
save this script below in a file '**test.py**' and make sure they're in the same directory. Or, download them from this repository. They are the same.



    import xml.etree.ElementTree as ET
    
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


**Some notes:** if there is no namespace specified in the `<XML>` tag at the begining of the XML document
simply just remove the namespace portion from the code or make `rootKey = ''`. If there are multiple namespaces, adapt the code accordingly.

Example:

    rootKey1 = './/{this:is:the:namespace1}'
    rootKey2 = './/{this:is:the:namespace2}'


There you have it, this is what works best for me and what I find to be the easiest. Hopefully you have found something of value here.



