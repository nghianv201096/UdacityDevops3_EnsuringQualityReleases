resource "azurerm_network_interface" "test" {
  name                = "${var.application_type}-${var.resource_type}-nic"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

data "azurerm_image" "ubuntu" {
  name                = var.image_name
  resource_group_name = var.image_resource_group_name
}

resource "azurerm_linux_virtual_machine" "test" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"
  size                = "Standard_DS1_v2"
  admin_username      = "${var.vm_username}"
  admin_password      = "${var.vm_password}"
  disable_password_authentication = false
  network_interface_ids = [azurerm_network_interface.test.id]
  
  source_image_id = data.azurerm_image.ubuntu.id

  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
}