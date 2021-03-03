from django.core.management.base import BaseCommand
import datetime
from apps.dms.documents.models import Documents
from apps.dms.documents.elastic_search import Elastic
from django.db.models import Q
from django.db.models.functions import Coalesce
import json
from django.utils import timezone


def doc_delete(doc):
    print("doc del")
    print(doc.id)
    try:
        doc.deleted = True
        # doc.deleted_at = datetime.now()
        doc.save()
    except Exception as e:
        print(e)


class Command(BaseCommand):
    help = 'Document Delete'

    def handle(self, *args, **options):
        current_date = datetime.datetime.now().date()
        print("current_date", current_date)
        documents = Documents.objects.filter(locked=False, deleted=False, archived=False, published=True,
                                             expiry_date__lt=current_date)

        for docs in documents:
            doc = Documents.objects.get(id=docs.id)
            if doc.action_upon_expiry == 2:
                def docdelete(doc):
                    doc.deleted = True
                    doc.deleted_at = timezone.now()
                    doc.save()

                docdelete(doc)

                if doc.parent_id:
                    doc = Documents.objects.filter(Q(id=doc.parent_id) | Q(parent=doc.parent_id)).order_by(
                        Coalesce('version', 'parent').desc()).first()

                    # process for elastic Search

                    tempmetas = json.loads(doc.metadata)
                    d = dict()
                    for tempmata in tempmetas:
                        d[tempmata['name']] = tempmata['value']

                    # process
                    doc.metadata = json.dumps(d)

                    Elastic.update(doc, doc.parent_id)
                else:
                    docId = doc.parent_id
                    documents = Documents.objects.filter(parent_id=doc.id)
                    for document in documents:
                        docdelete(document)

                    # process for elastic Search
                    tempmetas = json.loads(doc.metadata)
                    d = dict()
                    for tempmata in tempmetas:
                        d[tempmata['name']] = tempmata['value']

                    # process
                    doc.metadata = json.dumps(d)
                    Elastic.update(doc, doc.parent_id)
            elif doc.action_upon_expiry == 1:
                print(doc.id)
                doc.archived = True
                doc.archived_at = timezone.now()
                doc.save()
                if doc.parent_id:
                    parent = doc.parent
                    parent.archived = True
                    parent.archived_at = timezone.now()
                    parent.save()
                    all_files = Documents.objects.filter(Q(parent=parent))
                    if all_files.count():
                        for single_file in all_files:
                            single_file.archived = True
                            single_file.archived_at = timezone.now()
                            single_file.save()
                temp_metas = json.loads(doc.metadata)
                meta_dict = dict()

                for meta in temp_metas:
                    meta_dict[meta['name']] = meta['value']

                doc.metadata = json.dumps(meta_dict)
                Elastic.update(doc, doc.parent_id)
