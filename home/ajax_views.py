from django.views.generic import View
from django.http import JsonResponse


class UpdateProfileImageView(View):

    def post(self, request, *args, **kwargs):
        user = request.user

        profile_image = request.FILES.get('file')
        success = False
        if profile_image:
            user.profile_pic = profile_image
            user.save()
            success = True

            return JsonResponse({"image_url":user.image_url, "success":success}, safe=False)


class DeleteProfileImageView(View):

    def post(self, request, *args, **kwargs):
        user = request.user

        success = False
        if user:
            user.profile_pic = None
            user.save()
            success = True

            return JsonResponse({"image_url":user.image_url, "success":success}, safe=False)
