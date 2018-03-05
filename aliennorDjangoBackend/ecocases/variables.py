from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.conf import settings

image_fs = FileSystemStorage(location='/media/ecocases/')
esm_files_fs = FileSystemStorage(location='/media/esms/')
ecocase_image_fs = FileSystemStorage(location=os.path.join(
    settings.BASE_DIR, 'media/ecocases'))

aws_s3_ecocase_image_url = 'https://s3.eu-central-1.amazonaws.com/plf-aliennor/media/'
# aws_s3_ecocase_image_url = 'http://localhost:8080/plf-aliennor/media/'


case_type_choices = (
    ('Project', 'Project'),
    ('Proven cas', 'Proven cas'),
)

lavel_choices = (
    ('Business Level', 'Business Level'),
    ('Operation Level', 'Operation Level'),
    ('Business strategy', 'Business strategy'),
)

esms = [
    {
        "index": 1,
        "name": "parties-prenantes",
        "label": "Innover par les parties prenantes",
        "description": "Ce mécanisme questionne le réseau de parties prenantes à travers la valeur créée pour l'utilisateur, l'environnement, la société, l'conomie, et toute autre partie prenante significative."
    },
    {
        "index": 2,
        "name": "biomimétriste",
        "label": "Innover par le biomimétisme",
        "description": "Ce mécanisme souligne les ressemblances entre les systémes industriels humains et les systémes naturels, en séinspirant des stratégies de la nature pour faire naitre et maintenir la vie."
    },
    {
        "index": 3,
        "name": "modes-de-consommation",
        "label": "Innovate through sustainable mode of consumption",
        "description": "Ce mécanisme propose de questionner les usages non soutenables du systéme et déajuster le systéme aux utilisateurs finaux et aux spécificités du territoire (en terme de compétences, ressources etc.)"
    },
    {
        "index": 4,
        "name": "systèmes-produit-services",
        "label": "Innover par les Systémes Produit Services",
        "description": "Ce mécanisme pose la question de l'optimisation de la fonctionnalité de la matiére et de l'nergie consommées par le systéme (augmentation de l'intensité déusage, dématérialisation de l'offre) et de dissocier la propriété de l'acte de consommation."
    },
    {
        "index": 5,
        "name": "ressources-territoriales",
        "label": "Innover par les ressources territoriales",
        "description": "Ce mécanisme questionne sur l'intégration des capitaux territoriaux dans la stratégie et la conception de projet. Il interroge ainsi sur le capital naturel (ressources, services écosystémique), l'cosystéme industriel, le capital social (compétences), ainsi que le capital anthropique (infrastructure, moyens de production, financement)."
    },
    {
        "index": 6,
        "name": "circularité",
        "label": "Innover par la circularité",
        "description": "Ce mécanisme interroge sur les différentes possibilités de concevoir un systéme en boucle fermée, é travers des approches de recyclage, remanufacturing, ou déupgradabilité."
    },
    {
        "index": 7,
        "name": "nouvelles-technologies",
        "label": "Innover par les nouvelles technologies",
        "description": "Ce mécanisme questionne sur la possibilité déintégrer de nouveaux process et organisations de fabrication des produits, (fabrication additive, les fablabs é), de nouveaux matériaux (bio-matériaux, graphéne é)."
    }
]

domains = [
    {
        "label": "Energie"
    },
    {
        "label": "Mobilité"
    },
    {
        "label": "Habitat"
    },
    {
        "label": "Se nourir"
    }
]

# esm_dict = {
#     '1': 'Innover par les parties prenantes',
#     '2': 'Innover par le biomimétisme',
#     '3': 'Innover par les modes de consommation',
#     '4': 'Innover par les Systèmes Produits Services (PSS)',
#     '5': 'Innover par le territoire',
#     '6': 'Innover par la circularité',
#     '7': 'Innover par les nouvelles technologies'
# }

esm_dict = {
    '1': 'Innovate with stakeholders',
    '2': 'Innovate through biomimicry',
    '3': 'Innovate through sustainable mode of consumption',
    '4': 'Innovate through Product Service Systems',
    '5': 'Innovate through territorial resources',
    '6': 'Innovate through circularity',
    '7': 'Innovate through new technologies'
}


esm_link = [
    'ecocase/pdfs/esm1.pdf',
    'ecocase/pdfs/esm2.pdf',
    'ecocase/pdfs/esm3.pdf',
    'ecocase/pdfs/esm4.pdf',
    'ecocase/pdfs/esm5.pdf',
    'ecocase/pdfs/esm6.pdf',
    'ecocase/pdfs/esm7.pdf'
]

# esm_descriptions = [
#     {
#         "index": 1,
#         "title": "Innover par les parties prenantes",
#         "description": "Ce mécanisme questionne le réseau de parties prenantes à travers la valeur créée pour l'utilisateur, l'environnement, la société, l'conomie, et toute autre partie prenante significative."
#     },
#     {
#         "index": 2,
#         "title": "Innover par le biomimétisme",
#         "description": "Ce mécanisme souligne les ressemblances entre les systémes industriels humains et les systémes naturels, en séinspirant des stratégies de la nature pour faire naitre et maintenir la vie."
#     },
#     {
#         "index": 3,
#         "title": "Innover par les modes de consommation soutenable",
#         "description": "Ce mécanisme propose de questionner les usages non soutenables du systéme et déajuster le systéme aux utilisateurs finaux et aux spécificités du territoire (en terme de compétences, ressources etc.)"
#     },
#     {
#         "index": 4,
#         "title": "Innover par les Systémes Produit Services",
#         "description": "Ce mécanisme pose la question de l'optimisation de la fonctionnalité de la matiére et de l'nergie consommées par le systéme (augmentation de l'intensité déusage, dématérialisation de l'offre) et de dissocier la propriété de l'acte de consommation."
#     },
#     {
#         "index": 5,
#         "title": "Innover par les ressources territoriales",
#         "description": "Ce mécanisme questionne sur l'intégration des capitaux territoriaux dans la stratégie et la conception de projet. Il interroge ainsi sur le capital naturel (ressources, services écosystémique), l'cosystéme industriel, le capital social (compétences), ainsi que le capital anthropique (infrastructure, moyens de production, financement)."
#     },
#     {
#         "index": 6,
#         "title": "Innover par la circularité",
#         "description": "Ce mécanisme interroge sur les différentes possibilités de concevoir un systéme en boucle fermée, é travers des approches de recyclage, remanufacturing, ou déupgradabilité."
#     },
#     {
#         "index": 7,
#         "title": "Innover par les nouvelles technologies",
#         "description": "Ce mécanisme questionne sur la possibilité déintégrer de nouveaux process et organisations de fabrication des produits, (fabrication additive ...), de nouveaux matériaux (bio-matériaux, graphène ...)."
#     }
# ]

esm_descriptions = [
    {
        "index": 1,
        "title": "Innover par les parties prenantes",
        "description": "This mechanism questions the stakeholder network through the value created for the user, the environment, society, the economy, and any other significant stakeholder."
    },
    {
        "index": 2,
        "title": "Innover par le biomimétisme",
        "description": "This mechanism emphasizes the similarities between human industrial systems and natural systems, taking inspiration from nature's strategies for creating and sustaining life."
    },
    {
        "index": 3,
        "title": "Innover par les modes de consommation soutenable",
        "description": "This mechanism proposes to question the unsustainable uses of the system and to adjust the system to the end-users and the specificities of the territory (in terms of skills, resources, etc.)"
    },
    {
        "index": 4,
        "title": "Innover par les Systémes Produit Services",
        "description": "This mechanism raises the question of optimizing the functionality of the material and energy consumed by the system (increase of the intensity of use, dematerialization of the supply) and to dissociate the property from the act of consumption."
    },
    {
        "index": 5,
        "title": "Innover par les ressources territoriales",
        "description": "This mechanism questions the integration of territorial capital into strategy and project design. It questions natural capital (resources, ecosystem services), industrial co-system, social capital (skills), and anthropogenic capital (infrastructure, means of production, financing)."
    },
    {
        "index": 6,
        "title": "Innover par la circularité",
        "description": "This mechanism questions the different possibilities of designing a closed loop system, through recycling, remanufacturing or degradability approaches."
    },
    {
        "index": 7,
        "title": "Innover par les nouvelles technologies",
        "description": "This mechanism questions the possibility of disintegrating new processes and organizations manufacturing products, (additive manufacturing ...), new materials (bio-materials, graphene ...)."
    }
]

esm_vote_point = {
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
}

group_name_choices = {
    ('student', 'Student'),
    ('enteprise', 'Enterprise'),
    ('ecosd-scientist', 'Scientist'),
    ('project-scientist', 'Project scientist'),
}

esm_choices = (
  ('stakeholders','Innovate with stakeholders'),
  ('biomimicry','Innovate through biomimicry'),
  ('consumption','Innovate through sustainable mode of consumption'),
  ('product Service Systems','Innovate through Product Service Systems'),
  ('territorial resources','Innovate through territorial resources'),
  ('circularity','Innovate through circularity'),
  ('new technologies','Innovate through new technologies'),
)

vote_point_options = range(16)


def save_ecocase_images(title, images, path):
    joined_title = '_'.join(title.split(' '))
    image_url_list = []

    for count, x in enumerate(images):
        image_extension = x.name.split('.')[-1]
        print('extension:', image_extension)
        new_image_name = joined_title + '_' + \
            str(count) + '.' + image_extension
        print('image_name:', new_image_name)
        uploaded_image = ecocase_image_fs.save(new_image_name, x)
        print("uploaded image:", uploaded_image)
        image_url_list.append(path + new_image_name)
    return image_url_list
