from flask_wtf import FlaskForm
from wtforms import (IntegerField, RadioField, SelectField, SubmitField,PasswordField,
                     TextAreaField, TextField, ValidationError, validators, SelectMultipleField, widgets)
from wtforms.fields.html5 import EmailField

townstuple = [('Baldia Town', 'Baldia Town'),
        ('Bin Qasim Town', 'Bin Qasim Town'),
        ('Gadap Town', 'Gadap Town'),
        ('Gulberg Town', 'Gulberg Town'),
        ('Gulshan Town', 'Gulshan Town'),
        ('Jamshed Town', 'Jamshed Town'),
        ('Kemari Town', 'Kemari Town'),
        ('Korangi Town', 'Korangi Town'),
        ('Landhi Town', 'Landhi Town'),
        ('Liaquatabad Town', 'Liaquatabad Town'),
        ('Lyari Town', 'Lyari Town'),
        ('Malir Town', 'Malir Town'),
        ('New Karachi Town', 'New Karachi Town'),
        ('North Nazimabad Town', 'North Nazimabad Town'),
        ('Orangi Town', 'Orangi Town'),
        ('Saddar Town', 'Saddar Town'),
        ('Shah Faisal Town', 'Shah Faisal Town'),
        ('S.I.T.E. Town (Sindh Industrial & Trading Estate)',
        'S.I.T.E. Town (Sindh Industrial & Trading Estate)')]

def getAreas(array):

    areas = {'Baldia Town':
                ['Gulshan-e-Ghazi',
                'Ittehad Town',
                'Islam Nagar',
                'Nai Abadi',
                'Saeedabad',
                'Muslim Mujahid Colony',
                'Muhajir Camp',
                'Rasheedabad'],
            
            'Bin Qasim Town': 
                [ 'Ibrahim Hyderi',
                'Rehri',
                'Cattle Colony',
                'Qaidabad',
                'Landhi Colony',
                'Gulshan-e-Hadeed',
                'Gaghar'],
            
            'Gadap Town':    
                ['Murad Memon Goth',
                'Darsano Chana',
                'Gadap',
                'Gujro',
                'Songal',
                'Maymarabad',
                'Yousuf Goth',
                'Manghopir'],
            
            'Gulberg Town':
                [ 'Azizabad',
                'Karimabad',
                'Aisha Manzil',
                'Ancholi',
                'Naseerabad',
                'Yaseenabad',
                'Water Pump',
                'Shafiq Mill Colony'],
            
            'Gulshan Town':    
                [ 'ZIA COLONY',
                'Delhi Mercantile Society',
                'Civic Centre',
                'Pir Ilahi Buksh Colony',
                'Essa Nagri',
                'Gulshan-e-Iqbal',
                'Gillani Railway Station',
                'Dalmia',
                'Jamali Colony',
                'Gulshan-e-Iqbal II',
                'Pehlwan Goth',
                'Matrovil Colony',
                'Gulzar-e-Hijri',
                'Safooran Goth',
                'Faisal Cant'],
            
            
            'Jamshed Town': 
                [ 'Akhtar Colony',
                'Manzoor Colony',
                'Azam Basti',
                'Chanesar Goth',
                'Mehmoodabad',
                'P.E.C.H.S I (Pakistan Employees Co-operative Housing Society)',
                'P.E.C.H.S II',
                'Jut Line',
                'Jacob Lines',
                'Jamshed Quarters',
                'Garden East',
                'Soldier Bazar',
                'Pakistan Quarters'],
            
            'Kemari Town':
                [ 'Kiamari',
                'Baba Bhit',
                'Machar Colony',
                'Maripur',
                'SherShah',
                'Gabo Pat'],
            
            'Korangi Town': 
                ['Bilal Colony',
                'Nasir Colony',
                'Chakra Goth',
                'Silver Town',
                'Hundred Quarters',
                'Gulzar Colony',
                'Korangi Sector 33',
                'Zaman Town',
                'Hasrat Mohani Colony',
                ' Bhatti Colony'],

            'Landhi Town':     
                ['Muzafarabad',
                'Muslimabad',
                'Dawood Chowrangi',
                'Moinabad',
                'Sharafi Goth',
                'Bhutto Nagar',
                'Khawaja Ajmeer Colony',
                'Landhi',
                'Awami Colony',
                'Burmee Colony',
                'Korangi',
                'Sherabad'],
            
            'Liaquatabad Town':
                [ 'Rizvia Society (R.C.H.S.)',
                'Firdous Colony',
                'Sharifabad',
                'Commercial Area',
                'Abbasi Shaheed'],
            
            'Lyari Town':    
                ['Agra Taj Colony',
                'Daryaabad',
                'Nawabad',
                'Khada Memon Society',
                'Baghdadi',
                'Baghdadi',
                'Shah Baig Line',
                'Bihar Colony',
                'Ragiwara',
                'Singo Line',
                'Chakiwara',
                'Allama Iqbal Colony'],
            
            'Malir Town':
                [ 'Model Colony',
                'Kala Board',
                'Saudabad',
                'Khokhra Par',
                'Jafar-e-Tayyar',
                'Gharibabad',
                'Ghazi Brohi Goth'],
            
            'New Karachi Town':
                ['North Karachi',
                'Sir Syed Colony',
                'Fatima Jinnah Colony',
                'Godhra',
                'Abu Zar Ghaffari',
                'Hakim Ahsan',
                'Madina Colony',
                'Faisal Colony',
                'Khamiso Goth',
                'Mustufa Colony',
                'Khawaja Ajmeer Nagri',
                'Gulshan-e-Saeed',
                'Shah Nawaz Bhutto Colony'],
            
            'North Nazimabad Town':
                ['Paposh Nagar',
                'Pahar Ganj',
                'Khandu Goth',
                'Hyderi',
                'Sakhi Hassan',
                'Farooq-e-Azam',
                'Nusrat Bhutto Colony',
                'Shadman Town',
                'Buffer Zone',
                'Buffer Zone II'],
            
            'Orangi Town':
                [ 'Mominabad',
                'Haryana Colony',
                'Hanifabad',
                'Mohammad Nagar',
                'Madina Colony',
                'Ghaziabad',
                'Chisti Nagar',
                'Bilal Colony/sector 14 & 15',
                'Iqbal Baloch Colony',
                'Gabol Colony',
                'Data Nagar',
                'Mujahidabad',
                'Baloch Goth'],
            
            'Saddar Town':
                [ 'Old Haji Camp',
                'Garden',
                'Kharadar',
                'City Railway Colony',
                'Nanak Wara',
                'Gazdarabad',
                'Millat Nagar/Islam Pura',
                'Saddar',
                'Civil Line',
                'Clifton',
                'Kehkashan'
                'Dehli Colony'],
            
            'Shah Faisal Town':
                ['Natha Khan Goth',
                'Sadat Colony',
                'Dirg Colony',
                'Reta Plot',
                'Moria Khan Goth',
                'Rafa-e-Aam Society',
                'Al-Falah Society',
                'PAF',
                'Drig Road/Air Port'],
            
            'S.I.T.E. Town (Sindh Industrial & Trading Estate)':
                ['Pak Colony',
                'Old Golimar',
                'Jahanabad',
                'Metrovil',
                'Bhawani Chali',
                'Frontier Colony',
                'Banaras Colony']
            }
    arr = []
    for i in array:
        for j in areas[i]:
            arr.append(j)
        
    return arr


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class DonorsForm(FlaskForm): #Form Class

    towns = MultiCheckboxField('Select Town',[validators.DataRequired("Please Select Town.")] ,choices = townstuple)
    days = IntegerField("How long your package would last?",[validators.DataRequired("Please enter time")])  
    name = TextField("Donor's Organization Name",[validators.DataRequired("Please enter Name.")])
    city = TextField("City ",[validators.DataRequired("Please enter City.")])  
    username = TextField("Unique Username",[validators.DataRequired("Enter Username.")])  
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = EmailField("Email ",[validators.DataRequired("Enter Email.")])
    phone = IntegerField("Phone Number",[validators.DataRequired("Enter Phone Number")])  
    address = TextField("Organization's address",[validators.DataRequired("Please enter Address.")])
  
    submit = SubmitField("Submit")  

def getDonorsjson(username, password, name, email, phone, address, towns):
    donorsjson = {
        "username": username,
        "password": password,
        "organization name": name,
        "Email": email,
        "phone":phone,
        "address": address,
        "areas": towns,
        "requests":[""]
        }
    return donorsjson