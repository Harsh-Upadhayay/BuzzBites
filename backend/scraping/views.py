# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from scrapyd_api import ScrapydAPI
from decouple import config

scrapyd = ScrapydAPI(config('SCRAPYD_URL'))  

class DaemonStatusAPIView(APIView):
    def get(self, request):
        try:
            daemon_status = scrapyd.daemon_status()
            return Response(daemon_status, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddVersionAPIView(APIView):
    def post(self, request):
        project_name = request.data.get('project')
        version = request.data.get('version')
        egg_file_path = request.FILES.get('egg')

        if not project_name or not version or not egg_file_path:
            return Response({'error': 'Project name, version, and egg file are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scrapyd.add_version(project_name, version, egg_file_path)
            return Response({'success': f'Version {version} of project {project_name} added successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ScheduleSpiderAPIView(APIView):
    def get(self, request):
            project_name = request.query_params.get('project')
            spider_name = request.query_params.get('spider')
            spider_args = {}

            # Extract spider arguments from query parameters
            for param in request.query_params:
                if param not in ['project', 'spider']:
                    spider_args[param] = request.query_params[param]

            if not project_name or not spider_name:
                return Response({'error': 'Project name and spider name are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                job_id = scrapyd.schedule(project_name, spider_name, **spider_args)
                return Response({'success': f'Spider {spider_name} scheduled successfully', 'job_id': job_id}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CancelSpiderAPIView(APIView):
    def get(self, request):
        project_name = request.query_params.get('project')
        job_id = request.data.get('job')

        if not project_name or not job_id:
            return Response({'error': 'Project name and job ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scrapyd.cancel(project_name, job_id)
            return Response({'success': f'Spider job {job_id} canceled successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListProjectsAPIView(APIView):
    def get(self, request):
        try:
            projects = scrapyd.list_projects()
            return Response({'projects': projects}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListVersionsAPIView(APIView):
    def get(self, request):
        project_name = request.query_params.get('project')

        if not project_name:
            return Response({'error': 'Project name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            versions = scrapyd.list_versions(project_name)
            return Response({'versions': versions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListSpidersAPIView(APIView):
    def get(self, request):
        project_name = request.query_params.get('project')

        if not project_name:
            return Response({'error': 'Project name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            spiders = scrapyd.list_spiders(project_name)
            return Response({'spiders': spiders}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListJobsAPIView(APIView):
    def get(self, request):
        project_name = request.query_params.get('project')

        try:
            jobs = scrapyd.list_jobs(project_name)
            return Response({'jobs': jobs}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteVersionAPIView(APIView):
    def get(self, request):
        project_name = request.query_params.get('project')
        version = request.query_params.get('version')

        if not project_name or not version:
            return Response({'error': 'Project name and version are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scrapyd.delete_version(project_name, version)
            return Response({'success': f'Version {version} of project {project_name} deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProjectAPIView(APIView):
    def post(self, request):
        project_name = request.data.get('project')

        if not project_name:
            return Response({'error': 'Project name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scrapyd.delete_project(project_name)
            return Response({'success': f'Project {project_name} deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
