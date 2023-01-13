def image_upload_path(instance, file_name):
    file_folder = "Profile_images"
    return f"{instance.username}/{file_folder}/{file_name}"

def default_profile_image():
    return "default/user-default.png"

def default_cover_image():
    return "default/cover-default.png"

def cover_image_upload_path(instance, file_name):
    file_folder = "Cover_images"
    return f"{instance.username}/{file_folder}/{file_name}"