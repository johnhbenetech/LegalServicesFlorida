# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0008_auto_20170524_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='counties',
            field=models.CharField(choices=[('alachua', 'Alachua'), ('baker', 'Baker'), ('bay', 'Bay'), ('bradford', 'Bradford'), ('brevard', 'Brevard'), ('broward', 'Broward'), ('calhoun', 'Calhoun'), ('charlotte', 'Charlotte'), ('citrus', 'Citrus'), ('clay', 'Clay'), ('collier', 'Collier'), ('columbia', 'Columbia'), ('desoto', 'DeSoto'), ('dixie', 'Dixie'), ('duval', 'Duval'), ('escambia', 'Escambia'), ('flagler', 'Flagler'), ('franklin', 'Franklin'), ('gadsden', 'Gadsden'), ('gilchrist', 'Gilchrist'), ('glades', 'Glades'), ('gulf', 'Gulf'), ('hamilton', 'Hamilton'), ('hardee', 'Hardee'), ('hendry', 'Hendry'), ('hernando', 'Hernando'), ('highlands', 'Highlands'), ('hillsborough', 'Hillsborough'), ('holmes', 'Holmes'), ('indian river', 'Indian River'), ('jackson', 'Jackson'), ('jefferson', 'Jefferson'), ('lafayette', 'Lafayette'), ('lake', 'Lake'), ('lee', 'Lee'), ('leon', 'Leon'), ('levy', 'Levy'), ('liberty', 'Liberty'), ('madison', 'Madison'), ('manatee', 'Manatee'), ('marion', 'Marion'), ('martin', 'Martin'), ('miami-dade', 'Miami-Dade'), ('monroe', 'Monroe'), ('nassau', 'Nassau'), ('okaloosa', 'Okaloosa'), ('okeechobee', 'Okeechobee'), ('orange', 'Orange'), ('osceola', 'Osceola'), ('palm_beach', 'Palm Beach'), ('pasco', 'Pasco'), ('pinellas', 'Pinellas'), ('polk', 'Polk'), ('putnam', 'Putnam'), ('santa_rosa', 'Santa Rosa'), ('sarasota', 'Sarasota'), ('seminole', 'Seminole'), ('st_johns', 'St. Johns'), ('st_lucie', 'St. Lucie'), ('sumter', 'Sumter'), ('suwannee', 'Suwannee'), ('taylor', 'Taylor'), ('union', 'Union'), ('volusia', 'Volusia'), ('wakulla', 'Wakulla'), ('walton', 'Walton'), ('washington', 'Washington')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='website_url',
            field=models.CharField(max_length=255, null=True, verbose_name='Website URL'),
        ),
        migrations.AlterField(
            model_name='providerupdate',
            name='counties',
            field=models.CharField(choices=[('alachua', 'Alachua'), ('baker', 'Baker'), ('bay', 'Bay'), ('bradford', 'Bradford'), ('brevard', 'Brevard'), ('broward', 'Broward'), ('calhoun', 'Calhoun'), ('charlotte', 'Charlotte'), ('citrus', 'Citrus'), ('clay', 'Clay'), ('collier', 'Collier'), ('columbia', 'Columbia'), ('desoto', 'DeSoto'), ('dixie', 'Dixie'), ('duval', 'Duval'), ('escambia', 'Escambia'), ('flagler', 'Flagler'), ('franklin', 'Franklin'), ('gadsden', 'Gadsden'), ('gilchrist', 'Gilchrist'), ('glades', 'Glades'), ('gulf', 'Gulf'), ('hamilton', 'Hamilton'), ('hardee', 'Hardee'), ('hendry', 'Hendry'), ('hernando', 'Hernando'), ('highlands', 'Highlands'), ('hillsborough', 'Hillsborough'), ('holmes', 'Holmes'), ('indian river', 'Indian River'), ('jackson', 'Jackson'), ('jefferson', 'Jefferson'), ('lafayette', 'Lafayette'), ('lake', 'Lake'), ('lee', 'Lee'), ('leon', 'Leon'), ('levy', 'Levy'), ('liberty', 'Liberty'), ('madison', 'Madison'), ('manatee', 'Manatee'), ('marion', 'Marion'), ('martin', 'Martin'), ('miami-dade', 'Miami-Dade'), ('monroe', 'Monroe'), ('nassau', 'Nassau'), ('okaloosa', 'Okaloosa'), ('okeechobee', 'Okeechobee'), ('orange', 'Orange'), ('osceola', 'Osceola'), ('palm_beach', 'Palm Beach'), ('pasco', 'Pasco'), ('pinellas', 'Pinellas'), ('polk', 'Polk'), ('putnam', 'Putnam'), ('santa_rosa', 'Santa Rosa'), ('sarasota', 'Sarasota'), ('seminole', 'Seminole'), ('st_johns', 'St. Johns'), ('st_lucie', 'St. Lucie'), ('sumter', 'Sumter'), ('suwannee', 'Suwannee'), ('taylor', 'Taylor'), ('union', 'Union'), ('volusia', 'Volusia'), ('wakulla', 'Wakulla'), ('walton', 'Walton'), ('washington', 'Washington')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='providerupdate',
            name='website_url',
            field=models.CharField(max_length=255, null=True, verbose_name='Website URL'),
        ),
    ]
