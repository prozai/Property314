from flask import request, session, flash
from app import session
from app.entity.models import Property
import os
from datetime import datetime

# Create Property Listing
class createPropertyController:
    def REA_createProperty():
        try:
            if request.method == 'POST':
                propertyname = request.form['propertyname']
                propertytype = request.form['propertytype']
                district = request.form['district']
                bedroom_no = request.form['bedroom_no']
                price = request.form['price']
                psf = request.form['psf']
                image_file = request.files['image_url']

                if image_file:
                    new_property = Property(user_id=1,  # session['user_id']
                                            propertyname=propertyname,
                                            propertytype=propertytype,
                                            district=district,
                                            bedroom_no=bedroom_no,
                                            price=price,
                                            psf=psf,
                                            listing_date=datetime.now().date(),
                                            date_sold=None,
                                            image_url=None,
                                            sold=False)
                    session.add(new_property)
                    session.commit()

                    propertyid = new_property.ID
                    filename = f"{propertyid}.{image_file.filename.split('.')[-1]}"
                    upload_folder = './app/static/uploads/properties/'
                    path = './static/uploads/properties/'
                    image_file.save(os.path.join(upload_folder, filename))
                    image_path = os.path.join(path, filename)

                    new_property.image_url = image_path
                    session.commit()

                    flash("Added successfully!")

                else:
                    image_path = None

        except Exception as e:
            print("Error creating property:", str(e))

# REA View Property Listings
class viewPropertiesController:
    def REA_viewProperties():
        try:
            properties = session.query(Property).filter_by(user_id=1).all()  # session['user_id']
            return properties

        except Exception as e:
            print("Error retrieving property listings:", str(e))

# Update Property Listing
class updatePropertyController:
    def REA_updateProperty(id):
        try:
            if request.method == 'POST':
                propertyname = request.form['propertyname']
                propertytype = request.form['propertytype']
                district = request.form['district']
                bedroom_no = request.form['bedroom_no']
                price = request.form['price']
                psf = request.form['psf']
                image_file = request.files.get('image_url')

                updateProperty = session.query(Property).filter_by(ID=id).first()

                if updateProperty:
                    updateProperty.propertyname = propertyname
                    updateProperty.propertytype = propertytype
                    updateProperty.district = district
                    updateProperty.bedroom_no = bedroom_no
                    updateProperty.price = price
                    updateProperty.psf = psf
                    updateProperty.listing_date = datetime.now().date()

                    if image_file:
                        filename = f"{updateProperty.ID}.{image_file.filename.split('.')[-1]}"
                        upload_folder = './app/static/uploads/properties/'
                        path = './static/uploads/properties/'
                        image_file.save(os.path.join(upload_folder, filename))
                        image_path = os.path.join(path, filename)
                        updateProperty.image_url = image_path

                    session.commit()
                    flash("Updated successfully!")
                else:
                    flash("Property not found")

            property = session.query(Property).filter_by(ID=id).first()
            return property

        except Exception as e:
            print("Error updating property:", str(e))

# Delete Property Listing
class deletePropertyController:
    def REA_deleteProperty(id):
        try:
            property = session.query(Property).filter_by(ID=id).first()
            if property:
                # Remove the associated image file if it exists
                if property.image_url:
                    upload_folder = './app/static/uploads/properties/'
                    image_path = os.path.join(upload_folder, property.image_url.split("/")[-1])
                    if os.path.exists(image_path):
                        os.remove(image_path)

                session.delete(property)
                session.commit()
                flash("Deleted successfully!")
            else:
                flash("Property not found")

        except Exception as e:
            print("Error deleting property:", str(e))