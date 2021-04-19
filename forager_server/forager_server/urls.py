"""forager_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from forager_server_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_datasets',
         views.get_datasets,
         name='get_datasets'),
    path('api/start_cluster',
         views.start_cluster,
         name='start_cluster'),
    path('api/cluster/<slug:cluster_id>',
         views.get_cluster_status,
         name='get_cluster_status'),
    path('api/stop_cluster/<slug:cluster_id>',
         views.stop_cluster,
         name='stop_cluster'),
    path('api/create_index/<slug:dataset_name>',
         views.create_index,
         name='create_index'),
    path('api/index/<slug:index_id>',
         views.get_index_status,
         name='get_index_status'),
    path('api/download_index/<slug:index_id>',
         views.download_index,
         name='download_index'),
    path('api/delete_index/<slug:index_id>',
         views.delete_index,
         name='delete_index'),
    path('api/create_dataset',
         views.create_dataset,
         name='create_dataset'),
    path('api/dataset/<slug:dataset_name>',
         views.get_dataset_info,
         name='get_dataset_info'),
    path('api/get_users_and_categories/<slug:dataset_name>',
         views.get_users_and_categories,
         name='get_users_and_categories'),
    path('api/get_next_images/<slug:dataset_name>',
         views.get_next_images,
         name='get_next_images'),
    path('api/get_annotations/<slug:dataset_name>',
         views.get_annotations,
         name='get_annotations'),
    path('api/get_annotations_summary/<slug:dataset_name>',
         views.get_annotations_summary,
         name='get_annotations_summary'),
    path('api/dump_annotations/<slug:dataset_name>',
         views.dump_annotations,
         name='dump_annotations'),
    path('api/get_conflicts/<slug:dataset_name>',
         views.get_annotation_conflicts,
         name='get_annotation_conflicts'),
    path('api/add_annotation/<slug:dataset_name>/<slug:image_identifier>',
         views.add_annotation,
         name='add_annotation'),
    path('api/delete_annotation/<slug:dataset_name>/<slug:image_identifier>/<slug:ann_identifier>',
         views.delete_annotation,
         name='delete_annotation'),
    path('api/lookup_knn/<slug:dataset_name>',
         views.lookup_knn,
         name='lookup_knn'),
    path('api/query_svm/<slug:dataset_name>',
         views.lookup_svm,
         name='query_svm'),
    path('api/get_google/<slug:dataset_name>',
         views.get_google,
         name='get_google'),
    path('api/active_batch/<slug:dataset_name>',
         views.active_batch,
         name='active_batch'),
    path('api/import_annotations/<slug:dataset_name>',
         views.import_annotations,
         name='import_annotations'),
    path('api/generate_embedding_v2',
         views.generate_embedding_v2,
         name='generate_embedding_v2'),
    path('api/generate_text_embedding_v2',
         views.generate_text_embedding_v2,
         name='generate_text_embedding_v2'),
    path('api/query_knn_v2/<slug:dataset_name>',
         views.query_knn_v2,
         name='query_knn_v2'),
    path('api/train_svm_v2/<slug:dataset_name>',
         views.train_svm_v2,
         name='train_svm_v2'),
    path('api/query_svm_v2/<slug:dataset_name>',
         views.query_svm_v2,
         name='query_svm_v2'),
    path('api/get_next_images_v2/<slug:dataset_name>',
         views.get_next_images_v2,
         name='get_next_images_v2'),
    path('api/get_dataset_info_v2/<slug:dataset_name>',
         views.get_dataset_info_v2,
         name='get_dataset_info_v2'),
    path('api/get_annotations_v2',
         views.get_annotations_v2,
         name='get_annotations_v2'),
    path('api/add_annotations_v2',
         views.add_annotations_v2,
         name='add_annotations_v2'),
    path('api/delete_category_v2',
         views.delete_category_v2,
         name='delete_category_v2'),
    path('api/update_category_v2',
         views.update_category_v2,
         name='update_category_v2'),
    path('api/get_category_counts_v2/<slug:dataset_name>',
         views.get_category_counts_v2,
         name='get_category_counts_v2'),
    path('api/train_model_v2/<slug:dataset_name>',
         views.create_model,
         name='create_model'),
    path('api/model_v2/<slug:model_id>',
         views.get_model_status,
         name='get_model_status'),
    path('api/train_model_v2/<slug:dataset_name>',
         views.create_model,
         name='create_model'),
]
