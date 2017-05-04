from django.core.management.base import BaseCommand
import json, MySQLdb


class Command(BaseCommand):
    help = 'Command to be called to format a SQL dump of the old system into a way that django can import'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', nargs=1, type=str)
        parser.add_argument('password', nargs=1, type=str)
        parser.add_argument('database', nargs=1, type=str)

    def handle(self, *args, **options):

        item_count = 3
        item_type_count = 3

        username = options['username'][0]
        password = options['password'][0]
        database = options['database'][0]

        # Database connection information
        db = MySQLdb.connect(user=username, passwd=password, db=database)
        outputFile = "old.json"

        c = db.cursor(MySQLdb.cursors.DictCursor)


        # Handle Items

        items = []
        itemTypes = []
        itemTypeList={}

        c.execute("""SELECT * FROM items""")

        for i in range(c.rowcount):
            row = c.fetchone()

            if row['description'] not in itemTypeList:
                itemTypeName = row['description']


                itemTypeList[itemTypeName] = item_type_count

                itemType = {}
                itemType["model"] = "backend.itemType"
                itemType["pk"] = item_type_count
                itemType["fields"] = {}
                itemType["fields"]['name'] = row['description']
                itemType["fields"]['description'] = row['type']
                itemType["fields"]['needsSignature'] = row['secondFormID']

                item = {}

                item['fields'] = {}
                item["model"] = "backend.item"
                item["pk"] = item_count
                item['fields']["barcode"] = row['barcode']
                item['fields']["location"] = row['location']
                item['fields']["serial"] = row['serial']
                item['fields']['ItemTypeID'] = item_type_count

                item_type_count += 1
                item_count += 1

                items.append(item)
                itemTypes.append(itemType)


            else:

                itemTypeName = row['description']

                item = {}

                item["model"] = "backend.item"
                item["pk"] = item_count
                item['fields'] = {}
                item['fields']["barcode"] = row['barcode']
                item['fields']["location"] = row['location']
                item['fields']["serial"] = row['serial']
                item['fields']['ItemTypeID'] = itemTypeList[itemTypeName]

                items.append(item)

                item_count += 1
        merged_list = itemTypes + items
        with open(outputFile, 'w') as outfile:
            json.dump(merged_list, outfile, indent=4)
        print("" + str(len(itemTypes)) + " Item Types and " + str(len(items)) + " Items added to the json file and "
                                                                                "ready for import")




