from selenium.webdriver.common.by import By


class InventoryPageLocators(object):
    ADD_TO_CART_BUTTON = {"by": By.CLASS_NAME, "value": "btn_inventory"}
    INVENTORY_ITEM = {"by": By.CLASS_NAME, "value": "inventory_item"}
    ADD_TO_CART_FIRST = {"by": By.ID, "value": "add-to-cart-sauce-labs-backpack"}
    SHOPPING_CART_BADGE = {"by": By.CLASS_NAME, "value": "shopping_cart_badge"}
    SHOPPING_CART_LINK = {"by": By.CLASS_NAME, "value": "shopping_cart_link"}
    SELECT_SORT = {"by": By.CLASS_NAME, "value": "product_sort_container"}
    ITEM_NAME = {"by": By.CLASS_NAME, "value": "inventory_item_name"}
    ITEM_DESCRIPTION = {"by": By.CLASS_NAME, "value": "inventory_item_desc"}
    ITEM_PRICE = {"by": By.CLASS_NAME, "value": "inventory_item_price"}
    ITEM_LINK = {"by": By.TAG_NAME, "value": "a"}
