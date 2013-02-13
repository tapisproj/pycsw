# -*- coding: UTF-8 -*-

from lxml import etree
import metadata
import util


def dispatch_update(context, repository, config, project_id):
    p = repository.session.connection()\
        .execute('select name, description, created_at, updated_at from projects where id = %s', project_id)\
        .first()
    xml_id = "lv.vraa.tapis:{}".format(project_id)
    xml = plu_md_template.format(id=xml_id,
                                 contact_name=config.get('metadata:inspire', 'contact_name'),
                                 email=config.get('metadata:inspire', 'contact_email'),
                                 organization=config.get('metadata:main', 'provider_name'),
                                 date=p.created_at.date(), document_name=p.name, abstract=p.description,
                                 wms_url="http://tapisapp.alise.lv:8087/geoserver/inspire_{}/wms".format(project_id))
    exml = etree.fromstring(xml)
    record = metadata.parse_record(context, exml, repository)
    for rec in record:
        if len(repository.query_ids(ids=[xml_id])) == 0:
            repository.insert(rec, 'local', util.get_today_and_now())
        else:
            repository.update(rec)
    return 'text/plain', 'ok'

plu_md_template = u'''
<gmd:MD_Metadata xmlns="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd">
    <gmd:fileIdentifier>
        <gco:CharacterString>{id}</gco:CharacterString>
    </gmd:fileIdentifier>
    <gmd:language>
        <gmd:LanguageCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#LanguageCode" codeListValue="lvl">lvl</gmd:LanguageCode>
    </gmd:language>
    <gmd:hierarchyLevel>
        <gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode" codeListValue="dataset">dataset</gmd:MD_ScopeCode>
    </gmd:hierarchyLevel>
    <gmd:contact>
        <gmd:CI_ResponsibleParty>
            <gmd:individualName>
                <gco:CharacterString>{contact_name}</gco:CharacterString>
            </gmd:individualName>
            <gmd:organisationName>
                <gco:CharacterString>{organization}</gco:CharacterString>
            </gmd:organisationName>
            <gmd:contactInfo>
                <gmd:CI_Contact>
                    <gmd:address>
                        <gmd:CI_Address>
                            <gmd:electronicMailAddress>
                                <gco:CharacterString>{email}</gco:CharacterString>
                            </gmd:electronicMailAddress>
                        </gmd:CI_Address>
                    </gmd:address>
                </gmd:CI_Contact>
            </gmd:contactInfo>
            <gmd:role>
                <gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="pointOfContact">pointOfContact</gmd:CI_RoleCode>
            </gmd:role>
        </gmd:CI_ResponsibleParty>
    </gmd:contact>
    <gmd:dateStamp>
        <gco:Date>{date}</gco:Date>
    </gmd:dateStamp>
    <gmd:metadataStandardName>
        <gco:CharacterString>INSPIRE Metadata for Datasets</gco:CharacterString>
    </gmd:metadataStandardName>
    <gmd:metadataStandardVersion>
        <gco:CharacterString>DRAFT</gco:CharacterString>
    </gmd:metadataStandardVersion>
    <gmd:referenceSystemInfo>
        <gmd:MD_ReferenceSystem>
            <gmd:referenceSystemIdentifier>
                <gmd:RS_Identifier>
                    <gmd:code>
                        <gco:CharacterString/>
                    </gmd:code>
                    <gmd:codeSpace>
                        <gco:CharacterString/>
                    </gmd:codeSpace>
                </gmd:RS_Identifier>
            </gmd:referenceSystemIdentifier>
        </gmd:MD_ReferenceSystem>
    </gmd:referenceSystemInfo>
    <gmd:identificationInfo>
        <gmd:MD_DataIdentification>
            <gmd:citation>
                <gmd:CI_Citation>
                    <gmd:title>
                        <gco:CharacterString>{document_name}</gco:CharacterString>
                    </gmd:title>
                    <gmd:date>
                        <gmd:CI_Date>
                            <gmd:date>
                                <gco:Date>{date}</gco:Date>
                            </gmd:date>
                            <gmd:dateType>
                                <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication"/>
                            </gmd:dateType>
                        </gmd:CI_Date>
                    </gmd:date>
                    <gmd:date>
                        <gmd:CI_Date>
                            <gmd:date>
                                <gco:Date>{date}</gco:Date>
                            </gmd:date>
                            <gmd:dateType>
                                <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation"/>
                            </gmd:dateType>
                        </gmd:CI_Date>
                    </gmd:date>
                    <gmd:date>
                        <gmd:CI_Date>
                            <gmd:date>
                                <gco:Date>{date}</gco:Date>
                            </gmd:date>
                            <gmd:dateType>
                                <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision"/>
                            </gmd:dateType>
                        </gmd:CI_Date>
                    </gmd:date>
                    <gmd:identifier>
                        <gmd:MD_Identifier>
                            <gmd:code>
                                <gco:CharacterString>{id}</gco:CharacterString>
                            </gmd:code>
                        </gmd:MD_Identifier>
                    </gmd:identifier>
                </gmd:CI_Citation>
            </gmd:citation>
            <gmd:abstract>
                <gco:CharacterString>{abstract}</gco:CharacterString>
            </gmd:abstract>
            <gmd:pointOfContact>
                <gmd:CI_ResponsibleParty>
                    <gmd:organisationName>
                        <gco:CharacterString>{organization}</gco:CharacterString>
                    </gmd:organisationName>
                    <gmd:positionName>
                        <gco:CharacterString/>
                    </gmd:positionName>
                    <gmd:contactInfo>
                        <gmd:CI_Contact>
                            <gmd:phone>
                                <gmd:CI_Telephone>
                                    <gmd:voice>
                                        <gco:CharacterString/>
                                    </gmd:voice>
                                    <gmd:facsimile>
                                        <gco:CharacterString/>
                                    </gmd:facsimile>
                                </gmd:CI_Telephone>
                            </gmd:phone>
                            <gmd:address>
                                <gmd:CI_Address>
                                    <gmd:deliveryPoint>
                                        <gco:CharacterString/>
                                    </gmd:deliveryPoint>
                                    <gmd:city>
                                        <gco:CharacterString/>
                                    </gmd:city>
                                    <gmd:administrativeArea>
                                        <gco:CharacterString/>
                                    </gmd:administrativeArea>
                                    <gmd:postalCode>
                                        <gco:CharacterString/>
                                    </gmd:postalCode>
                                    <gmd:country>
                                        <gco:CharacterString/>
                                    </gmd:country>
                                    <gmd:electronicMailAddress>
                                        <gco:CharacterString>{email}</gco:CharacterString>
                                    </gmd:electronicMailAddress>
                                </gmd:CI_Address>
                            </gmd:address>
                            <gmd:onlineResource>
                                <gmd:CI_OnlineResource>
                                    <gmd:linkage>
                                        <gmd:URL/>
                                    </gmd:linkage>
                                </gmd:CI_OnlineResource>
                            </gmd:onlineResource>
                        </gmd:CI_Contact>
                    </gmd:contactInfo>
                    <gmd:role>
                        <gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="author"/>
                    </gmd:role>
                </gmd:CI_ResponsibleParty>
            </gmd:pointOfContact>
            <gmd:graphicOverview/>
            <gmd:descriptiveKeywords>
                <gmd:MD_Keywords>
                    <gmd:keyword>
                        <gco:CharacterString>1</gco:CharacterString>
                    </gmd:keyword>
                    <gmd:thesaurusName>
                        <gmd:CI_Citation>
                            <gmd:title>
                                <gco:CharacterString>GEMET - INSPIRE themes, version 1.0</gco:CharacterString>
                            </gmd:title>
                            <gmd:date>
                                <gmd:CI_Date>
                                    <gmd:date>
                                        <gco:Date>2008-06-01</gco:Date>
                                    </gmd:date>
                                    <gmd:dateType>
                                        <gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication">publication</gmd:CI_DateTypeCode>
                                    </gmd:dateType>
                                </gmd:CI_Date>
                            </gmd:date>
                        </gmd:CI_Citation>
                    </gmd:thesaurusName>
                </gmd:MD_Keywords>
            </gmd:descriptiveKeywords>
            <gmd:descriptiveKeywords>
                <gmd:MD_Keywords>
                    <gmd:keyword>
                        <gco:CharacterString>teritorialajs planojums</gco:CharacterString>
                    </gmd:keyword>
                    <gmd:thesaurusName>
                        <gmd:CI_Citation>
                            <gmd:title>
                                <gco:CharacterString>GEMET</gco:CharacterString>
                            </gmd:title>
                            <gmd:date>
                                <gmd:CI_Date>
                                    <gmd:date>
                                        <gco:Date>2012-09-19</gco:Date>
                                    </gmd:date>
                                    <gmd:dateType>
                                        <gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="">creation</gmd:CI_DateTypeCode>
                                    </gmd:dateType>
                                </gmd:CI_Date>
                            </gmd:date>
                        </gmd:CI_Citation>
                    </gmd:thesaurusName>
                </gmd:MD_Keywords>
            </gmd:descriptiveKeywords>
            <gmd:resourceConstraints>
                <gmd:MD_Constraints>
                    <gmd:useLimitation>
                        <gco:CharacterString>no conditions apply</gco:CharacterString>
                    </gmd:useLimitation>
                </gmd:MD_Constraints>
            </gmd:resourceConstraints>
            <gmd:resourceConstraints>
                <gmd:MD_LegalConstraints>
                    <gmd:accessConstraints>
                        <gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions">otherRestrictions</gmd:MD_RestrictionCode>
                    </gmd:accessConstraints>
                    <gmd:otherConstraints>
                        <gco:CharacterString>no limitations</gco:CharacterString>
                    </gmd:otherConstraints>
                </gmd:MD_LegalConstraints>
            </gmd:resourceConstraints>
            <gmd:spatialRepresentationType>
                <gmd:MD_SpatialRepresentationTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode" codeListValue=""/>
            </gmd:spatialRepresentationType>
            <gmd:spatialResolution>
                <gmd:MD_Resolution>
                    <gmd:equivalentScale>
                        <gmd:MD_RepresentativeFraction>
                            <gmd:denominator>
                                <gco:Integer>10000</gco:Integer>
                            </gmd:denominator>
                        </gmd:MD_RepresentativeFraction>
                    </gmd:equivalentScale>
                </gmd:MD_Resolution>
            </gmd:spatialResolution>
            <gmd:language>
                <gmd:LanguageCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#LanguageCode" codeListValue="eng"/>
            </gmd:language>
            <gmd:topicCategory>
                <gmd:MD_TopicCategoryCode>farming</gmd:MD_TopicCategoryCode>
            </gmd:topicCategory>
            <gmd:extent>
                <gmd:EX_Extent>
                    <gmd:geographicElement>
                        <gmd:EX_GeographicBoundingBox>
                            <gmd:westBoundLongitude>
                                <gco:Decimal>20.680</gco:Decimal>
                            </gmd:westBoundLongitude>
                            <gmd:eastBoundLongitude>
                                <gco:Decimal>28.160</gco:Decimal>
                            </gmd:eastBoundLongitude>
                            <gmd:southBoundLatitude>
                                <gco:Decimal>55.677</gco:Decimal>
                            </gmd:southBoundLatitude>
                            <gmd:northBoundLatitude>
                                <gco:Decimal>58.085</gco:Decimal>
                            </gmd:northBoundLatitude>
                        </gmd:EX_GeographicBoundingBox>
                    </gmd:geographicElement>
                    <gmd:temporalElement>
                        <gmd:EX_TemporalExtent>
                            <gmd:extent>
                                <gml:TimePeriod gml:id="Temporal">
                                    <gml:begin>
                                        <gml:TimeInstant gml:id="TemporalBegin">
                                            <gml:timePosition>2013-02-12</gml:timePosition>
                                        </gml:TimeInstant>
                                    </gml:begin>
                                    <gml:end>
                                        <gml:TimeInstant gml:id="TemporalEnd">
                                            <gml:timePosition>2013-02-12</gml:timePosition>
                                        </gml:TimeInstant>
                                    </gml:end>
                                </gml:TimePeriod>
                            </gmd:extent>
                        </gmd:EX_TemporalExtent>
                    </gmd:temporalElement>
                </gmd:EX_Extent>
            </gmd:extent>
        </gmd:MD_DataIdentification>
    </gmd:identificationInfo>
    <gmd:distributionInfo>
        <gmd:MD_Distribution>
            <gmd:distributionFormat>
                <gmd:MD_Format>
                    <gmd:name>
                        <gco:CharacterString/>
                    </gmd:name>
                    <gmd:version>
                        <gco:CharacterString/>
                    </gmd:version>
                </gmd:MD_Format>
            </gmd:distributionFormat>
            <gmd:transferOptions>
                <gmd:MD_DigitalTransferOptions>
                    <gmd:onLine>
                        <gmd:CI_OnlineResource>
                            <gmd:linkage>
                                <gmd:URL>{wms_url}</gmd:URL>
                            </gmd:linkage>
                            <gmd:function>
                                <gmd:CI_OnLineFunctionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue=""/>
                            </gmd:function>
                        </gmd:CI_OnlineResource>
                    </gmd:onLine>
                </gmd:MD_DigitalTransferOptions>
            </gmd:transferOptions>
        </gmd:MD_Distribution>
    </gmd:distributionInfo>
    <gmd:dataQualityInfo>
        <gmd:DQ_DataQuality>
            <gmd:scope>
                <gmd:DQ_Scope>
                    <gmd:level>
                        <gmd:MD_ScopeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="service">service</gmd:MD_ScopeCode>
                    </gmd:level>
                </gmd:DQ_Scope>
            </gmd:scope>
            <gmd:report>
                <gmd:DQ_DomainConsistency xsi:type="DQ_DomainConsistency_Type">
                    <gmd:measureIdentification>
                        <gmd:RS_Identifier>
                            <gmd:code>
                                <gco:CharacterString>Conformity_001</gco:CharacterString>
                            </gmd:code>
                            <gmd:codeSpace>
                                <gco:CharacterString>INSPIRE</gco:CharacterString>
                            </gmd:codeSpace>
                        </gmd:RS_Identifier>
                    </gmd:measureIdentification>
                    <gmd:result>
                        <gmd:DQ_ConformanceResult xsi:type="DQ_ConformanceResult_Type">
                            <gmd:specification>
                                <gmd:CI_Citation>
                                    <gmd:title>
                                        <gco:CharacterString>Pārbaude</gco:CharacterString>
                                    </gmd:title>
                                    <gmd:date>
                                        <gmd:CI_Date>
                                            <gmd:date>
                                                <gco:Date>2013-01-01</gco:Date>
                                            </gmd:date>
                                            <gmd:dateType>
                                                <gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication"/>
                                            </gmd:dateType>
                                        </gmd:CI_Date>
                                    </gmd:date>
                                </gmd:CI_Citation>
                            </gmd:specification>
                            <gmd:explanation>
                                <gco:CharacterString>See the referenced specification</gco:CharacterString>
                            </gmd:explanation>
                            <gmd:pass>
                                <gco:Boolean>true</gco:Boolean>
                            </gmd:pass>
                        </gmd:DQ_ConformanceResult>
                    </gmd:result>
                </gmd:DQ_DomainConsistency>
            </gmd:report>
            <gmd:lineage>
                <gmd:LI_Lineage>
                    <gmd:statement>
                        <gco:CharacterString>Izcelsme</gco:CharacterString>
                    </gmd:statement>
                </gmd:LI_Lineage>
            </gmd:lineage>
        </gmd:DQ_DataQuality>
    </gmd:dataQualityInfo>
</gmd:MD_Metadata>
'''
