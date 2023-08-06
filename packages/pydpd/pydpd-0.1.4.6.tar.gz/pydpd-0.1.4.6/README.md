## pydpd

### A DPD API wrapper (UK only I believe)

Create DPD shipments and generate parcel labels from within your application or webapp.

You will need a valid DPD account and have API access enabled (which can be done by calling 0121 275 7336)

## Features

* Check available services for a shipment
* Create a shipment 
* Generate labels in HTML, PDF or the raw printer data

## What's not possible (yet)

* Collections
* Swaps
* Extended Liability   
* Internation Shipments


## Installation

Download and install can be done through PyPi

```
pip install pydpd
```
or

```python
git clone https://github.com/lewis-morris/pydpd
cd pydpd
pip install -e .
```

>## IMPORTANT NOTE
> if you want to generate PDF versions of your labels you will have to install some additional software
> 
> ### Linux / Ubuntu
>  sudo apt-get install wkhtmltopdf
> ### Windows
> [Windows install guide](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)


## Pending Features

* Parcel Tracking 


## How to use

> Minimal working example
> 
```python
from pydpd import DPD, Parcel, Address

#create sender object
sender = Address(**{"name": "Mr Ship",
                    "organisation": "SuperShipCo",
                    "address1": "Ship Street",
                    "address2": "Shipton",
                    "postcode": "BR5 3DX"})
#create dpd object
dpd = DPD("[your dpd username]","[your dpd password]","[your dpd acc no]", sender)

#create a parcel definition
my_parcel = Parcel(**{"weight": 10,
                         "pcs": 2,
                         "name": "Boris",
                         "address1": "10 Downing Street",
                         "address2": "London",
                         "postcode": "SW1A 2AB"})

#book the delivery with "1^12" service - (Next day)  returns a delivery object
my_delivery = dpd.create_delivery(my_parcel,"1^12")

#get dpd PIL image label
my_delivery.get_png_labels(2)[0]

```

![Image](examples/nVNBt39IzpOmOg.png)

## Full Example 
I always find it best to learn by example so follow this jupyter notebook to see the flow. 

[Jupyter notebook examples](examples/dpd_examples.ipynb)

All classes have doc strings, so you can always check there if you get stuck.


## Contact

If you have any issues or just want to chat you can always email me at lewis.morris@gmail.com or open an issue.
