import sys
from pathlib import Path
import os
import json
from requests import Session
from requests.auth import HTTPBasicAuth
import re
import urllib3
from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from collections import OrderedDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def element_list_to_ordered_dict(elements):
    return [OrderedDict((element.tag, element.text) for element in row) for row in elements]

class axl(object):
    def __init__(self, username, password, cucm, cucm_version):
        cwd = os.path.dirname(os.path.abspath(__file__))
        if os.name == "posix":
            #wsdl = Path(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").as_uri()
            wsdl = "file://"+os.path.dirname(os.path.abspath(__file__))+"/schema/current/AXLAPI.wsdl"
        else:
            wsdl = str(Path("{cwd}/schema/{cucm_version}/AXLAPI.wsdl").absolute())
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(username, password)
        settings = Settings(
            strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True
        )
        transport = Transport(session=session, timeout=10, cache=SqliteCache())
        axl_client = Client(wsdl, settings=settings, transport=transport)

        self.wsdl = wsdl
        self.username = username
        self.password = password
        self.wsdl = wsdl
        self.cucm = cucm
        self.cucm_version = cucm_version
        self.UUID_PATTERN = re.compile(
            r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE
        )
        self.client = axl_client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            "https://"+cucm+":8443/axl/",
        )

    def sql_query(self, query):
        axl_resp = self.client.executeSQLQuery(sql=query)
        try:
            value = element_list_to_ordered_dict(serialize_object(axl_resp)["return"]["rows"])
            jsonList = []    
            for i in range(len(value)):
                jsonList.append(json.loads(json.dumps(value[i])))
            return jsonList

        except KeyError:
            # single tuple response
            value = element_list_to_ordered_dict(serialize_object(axl_resp)["return"]["row"])
            jsonList = []   
            for i in range(len(value)):
                jsonList.append(json.loads(json.dumps(value[i])))
            return jsonList

        except TypeError:
            # no SQL tuples
            return serialize_object(axl_resp)["return"]

    def sql_update(self, query):
        try:
            return self.client.executeSQLUpdate(query)["return"]
        except Fault as e:
            return e

    def getLocationNumbers(self, rborgunit):
        query = """select pkid,dnorpattern,description,fkroutepartition from numplan np
                where (np.description like UPPER('%-""" + rborgunit + """-%')) and (np.description like '%-iManage')
                and (np.pkid not in (Select np2.pkid from devicenumplanmap dnmp2, numplan np2 where dnmp2.fknumplan=np2.pkid))"""
        return self.sql_query(query = query) 

    def getNumberDetails(self, uc_phone_number):
        query = "select pkid,dnorpattern,description,fkroutepartition from numplan np where np.dnorpattern='" + uc_phone_number + "'"
        return self.sql_query(query = query)

    def getNumberFromUser(self, rbshortname):
        query = """select np.pkid,userid,np.dnorpattern from numplan np, devicenumplanmap dnmp, device d,enduserdevicemap edm, enduser e
                where np.pkid=dnmp.fknumplan and dnmp.fkdevice=d.pkid and e.pkid=edm.fkenduser and edm.fkdevice=d.pkid and
                UPPER(userid)=UPPER('""" + rbshortname + """') GROUP BY 1,2,3"""
        return self.sql_query(query = query)

    def getUserNotInImanageScope(self):
        query  = """select np.pkid ,userid,dnorpattern from device d,devicenumplanmap dnmp,numplan np,enduser e,enduserdevicemap edm 
                where d.pkid=dnmp.fkdevice and d.pkid=edm.fkdevice and e.pkid=edm.fkenduser and dnmp.fknumplan=np.pkid and dnorpattern 
                not like '%*%' and (Select count(edm2.pkid) from enduserdevicemap edm2,enduser e2 where edm2.fkenduser=e2.pkid and e2.userid=e.userid)=1 
                and e.fkdirectorypluginconfig is not null and UPPER(np.description) not like '%iManage%' group by 1,2,3 order by 2,3"""
        return self.sql_query(query = query)

    def checkAllDevices(self, rbshortname):
        query = """select d.name,moniker from device d,enduserdevicemap edm,enduser e,typemodel t where d.pkid=edm.fkdevice and 
                edm.fkenduser=e.pkid and d.tkmodel = t.enum and UPPER(userid)=UPPER('""" + rbshortname +"""')"""
        return self.sql_query(query = query)

    def checkDeskphone(self, userid):
        query = """select d.name from device d,enduserdevicemap edm,enduser e where d.pkid=edm.fkdevice and edm.fkenduser=e.pkid and 
                d.tkclass='254' and UPPER(userid)=UPPER('""" + userid + """')"""
        return self.sql_query(query = query)
    
    def createDeskphone(self, ucm_location, rbimsid, rbshortname):
        query = """insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, 
        fkcallingsearchspace, tkclass, fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, 
        tkdeviceprofile, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, 
        tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, 
        mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, 
        requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, 
        fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, fkcommondeviceconfig, 
        tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform, tkoutboundcallrollover, 
        tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, 
        tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, 
        tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, 
        hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, 
        usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, 
        usedevicepoolrdntransformcss, fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, 
        fkcallingsearchspace_cgpningressdn, earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, 
        fkwirelesslanprofilegroup, enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) 
        select REPLACE(name, '-""" + ucm_location + """-iManage', '"""+ rbimsid +"""'), SUBSTRING('iManage """ + rbshortname + """' FROM 1 FOR 50), 
        tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, '254', fkprocessnode, defaultdtmfcapability, 
        fklocation, tkproduct, (Select pkid from enduser where UPPER(userid)=UPPER('""" + rbshortname + """')), allowhotelingflag, 
        CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, 
        tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, 
        mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, 
        requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, 
        fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, fkcommondeviceconfig, 
        tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform , tkoutboundcallrollover, 
        tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, 
        tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, 
        tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, 
        tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, 
        fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
        usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
        fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
        earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
        enablecallroutingtordwhennoneisactive, fkwifihotspotprofile from device d where name like '%""" + ucm_location + """%' and tkclass in ('252')"""
        return self.sql_update(query = query)
    
    def checkPcBasedDeskphone(self, rbshortname):
        query="""select d.name from device d,enduserdevicemap edm,enduser e where d.pkid=edm.fkdevice and edm.fkenduser=e.pkid and 
        d.tkmodel=(Select enum from typemodel where moniker='MODEL_CLIENT_SERVICES_FRAMEWORK') and UPPER(userid)=UPPER('""" + rbshortname + """')"""
        return self.sql_query(query = query)

    def createPcBasedDeskphone(self, ucm_location, rbimsid, rbshortname):
        query="""insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, tkdeviceprofile, ikdevice_defaultprofile, 
            fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, 
            tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, 
            fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, 
            allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, 
            isstandard, resettoggle, tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, 
            fkcallingsearchspace_cgpntransform, tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, 
            srtpfallbackallowed, ispaienabled, isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss,
            usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, 
            fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, 
            sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
            usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) select UPPER(REPLACE(name, '-"""+ ucm_location + """-iManage', '""" + rbimsid + """')), 
            SUBSTRING('iManage """ + rbshortname + """' FROM 1 FOR 50), tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, 
            fkcallingsearchspace, fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, (Select pkid from enduser where 
            PPER(userid)=UPPER('""" + rbshortname + """')), allowhotelingflag, CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, 
            fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, 
            tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, 
            fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, 
            allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, 
            isstandard, resettoggle, tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, 
            fkcallingsearchspace_cgpntransform , tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, 
            tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, tksipprivacy, tksipassertedtype, 
            fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, 
            tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, 
            tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, fkvipre164transformation, 
            usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, 
            fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, fkcallingsearchspace_rdntransform, 
            enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, earlyoffersupportforvoicecall, 
            enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, enablecallroutingtordwhennoneisactive, 
            fkwifihotspotprofile from device d where name like '%"""+ ucm_location + """%' and tkclass in ('253', '252') and 
            d.tkmodel=(Select enum from typemodel where moniker='MODEL_CLIENT_SERVICES_FRAMEWORK')"""
        return self.sql_update(query = query)

    def checkIphoneBasedDeskphone(self, rbshortname):
        query="""select d.name from device d,enduserdevicemap edm,enduser e where d.pkid=edm.fkdevice and edm.fkenduser=e.pkid and d.tkmodel=(Select enum 
            from typemodel where moniker='MODEL_TIN_CAN_TOUCH') and UPPER(userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_query(query = query)

    def createIphoneBasedDeskphone(self, ucm_location, rbimsid, rbshortname):
        query="""insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, tkdeviceprofile, ikdevice_defaultprofile, 
            fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, 
            tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, 
            fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, 
            allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, 
            isstandard, resettoggle, tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, 
            fkcallingsearchspace_cgpntransform, tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, 
            srtpfallbackallowed, ispaienabled, isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, 
            usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, 
            fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, 
            sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
            usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) select UPPER(REPLACE(name, '-""" + ucm_location + """-iManage', '"""+rbimsid+"""')), 
            SUBSTRING('iManage """+rbshortname+"""' FROM 1 FOR 50), tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, (Select pkid from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""')), 
            allowhotelingflag, CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, 
            networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, 
            tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, 
            tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, 
            fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, 
            fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform , 
            tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, 
            isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, 
            tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, 
            tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, 
            fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
            usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile from device d where name like '%"""+ucm_location+"""%' and tkclass in ('253', '252') 
            and d.tkmodel=(Select enum from typemodel where moniker='MODEL_TIN_CAN_TOUCH')"""

    def checkAndroidBasedDeskphone(self, rbshortname):
        query= """select d.name from device d,enduserdevicemap edm,enduser e where d.pkid=edm.fkdevice and edm.fkenduser=e.pkid and d.tkmodel=(Select enum from typemodel 
            where moniker='MODEL_CISCO_DUAL_MODE_FOR_ANDROID') and UPPER(userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_query(query = query)

    def createAndroidBasedDeskphone(self, ucm_location, rbimsid, rbshortname):
        query = """insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, fkprocessnode,
            defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, tkdeviceprofile, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, 
            networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, 
            tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, 
            tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, 
            fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, 
            fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform, 
            tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, 
            isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, 
            tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, 
            tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, 
            fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
            usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) select UPPER(REPLACE(name, '-"""+ucm_location+"""-iManage', '"""+rbimsid+"""')), 
            SUBSTRING('iManage """+rbshortname+"""' FROM 1 FOR 50), tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, (Select pkid from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""')), 
            allowhotelingflag, CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, 
            networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, 
            tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, 
            tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, 
            fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, 
            fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform , 
            tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, 
            isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, 
            tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, 
            tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, 
            fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, 
            usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile from device d where name like '%"""+ucm_location+"""%' and 
            tkclass in ('253', '252') and d.tkmodel=(Select enum from typemodel where moniker='MODEL_CISCO_DUAL_MODE_FOR_ANDROID')"""
        return self.sql_update(query=query)

    def checkIpadBasedDeskphone(self, rbshortname):
        query = """select d.name from device d,enduserdevicemap edm,enduser e where d.pkid=edm.fkdevice and edm.fkenduser=e.pkid and d.tkmodel=(Select enum 
            from typemodel where moniker='MODEL_CISCO_JABBER_FOR_TABLET') and UPPER(userid)=UPPER('"""+ rbshortname +"""')"""
        return self.sql_query(query=query)

    def createIpadBasedDeskphone(self, ucm_location, rbimsid, rbshortname):
        query = """insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, tkdeviceprofile, ikdevice_defaultprofile, fkmediaresourcelist, 
            userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, 
            tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, 
            tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, 
            fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, 
            dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform, tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, 
            tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, 
            usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, 
            fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, 
            fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, 
            fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, fkcallingsearchspace_rdntransform, enablebfcp, 
            requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, 
            tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) 
            select UPPER(REPLACE(name, '-"""+ucm_location+"""-iManage', '"""+rbimsid+"""')), SUBSTRING('iManage """+rbshortname+"""' FROM 1 FOR 50), tkmodel, tkdeviceprotocol, 
            tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, 
            (Select pkid from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""')), allowhotelingflag, CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, 
            fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, 
            tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, 
            fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, 
            fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, tkreset, fkcommondeviceconfig, 
            tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform , tkoutboundcallrollover, 
            tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, tksipprivacy, 
            tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, 
            tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, 
            hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, 
            usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, 
            usedevicepoolrdntransformcss, fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, 
            earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, enablecallroutingtordwhennoneisactive, 
            fkwifihotspotprofile from device d where name like '%"""+ucm_location+"""%' and 
            tkclass in ('253', '252') and d.tkmodel=(Select enum from typemodel where moniker='MODEL_CISCO_JABBER_FOR_TABLET')"""
        return self.sql_update(query=query)

    def deletFromDevice(self, rbimsid):
        query= """delete from device where (UPPER(name) = UPPER('CSF"""+rbimsid+"""') or UPPER(name) = UPPER('TAB"""+rbimsid+"""' ) or UPPER(name) = UPPER('BOT"""+rbimsid+"""') or UPPER(name) = UPPER('TCT"""+rbimsid+"""')  
            or UPPER(name) like UPPER('"""+rbimsid+"""-%')) and description like 'iManage%'"""
        return self.sql_update(query=query)

    def deletePrimaryNumberassignment(self, rbshortname):
        query="""delete from endusernumplanmap where fkenduser=(Select pkid from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""')) and tkdnusage=1"""
        return self.sql_update(query=query)

    def createAllDevices(self, postcode, country, sidecode, rbshortname):
        query="""insert into device (name, description, tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, tkclass, fkprocessnode, 
            defaultdtmfcapability, fklocation, tkproduct, fkenduser, allowhotelingflag, tkdeviceprofile, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, 
            networkholdmohaudiosourceid, tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, 
            mtprequired, tknetworklocation, fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, 
            fksipprofile, rfc2833disabled, allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, 
            srtpallowed, isstandard, resettoggle, tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, 
            fkcallingsearchspace_cgpntransform, tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, 
            ispaienabled, isrpidenabled, tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, 
            tkstatus_audiblealertingidle, tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, 
            tkstatus_alwaysuseprimelineforvm, hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, 
            usedevicepoolcgpntransformcssintl, usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, 
            tkdevicetrustmode, usedevicepoolrdntransformcss, fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, 
            fkcallingsearchspace_cgpningressdn, earlyoffersupportforvoicecall, enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, 
            enablecallroutingtordwhennoneisactive, fkwifihotspotprofile) 
            select UPPER(REPLACE(name, '-LH-"""+postcode+"""-iManage', '"""+rbshortname+"""')), SUBSTRING('LH-"""+postcode+"""-"""+sidecode+""" """+rbshortname+"""' FROM 1 FOR 50), tkmodel, tkdeviceprotocol, tkprotocolside, fkdevicepool, fkphonetemplate, fkcallingsearchspace, 
            CASE WHEN tkclass='252' then '254' ELSE '1' END, fkprocessnode, defaultdtmfcapability, fklocation, tkproduct, (Select pkid from enduser where userid='"""+rbshortname+"""'), 
            allowhotelingflag, CASE WHEN tkclass='252' then '1' ELSE '0' END, ikdevice_defaultprofile, fkmediaresourcelist, userholdmohaudiosourceid, networkholdmohaudiosourceid, 
            tkcountry, tkuserlocale, fkcallingsearchspace_aar, fksoftkeytemplate, tkstatus_mlppindicationstatus, tkpreemption, tkstatus_builtinbridge, mtprequired, tknetworklocation, 
            fksecurityprofile, fkdialrules, fkcallingsearchspace_reroute, fkcallingsearchspace_refer, tkdtmfsignaling, requiredtmfreception, publickey, fksipprofile, rfc2833disabled, 
            allowcticontrolflag, sshpassword, sshuserid, fkcallingsearchspace_restrict, fkmatrix_presence, fkcommonphoneconfig, tkkeyauthority, srtpallowed, isstandard, resettoggle, 
            tkreset, fkcommondeviceconfig, tkstatus_devicemobilitymode, dndtimeout, tkdndoption, tkringsetting_dnd, isdualmode, fkcallingsearchspace_cgpntransform , 
            tkoutboundcallrollover, tkphonepersonalization, tkstatus_joinacrosslines, tkbarge, tkstatus_usetrustedrelaypoint, srtpfallbackallowed, ispaienabled, isrpidenabled, 
            tksipprivacy, tksipassertedtype, fkcallingsearchspace_cdpntransform, usedevicepoolcdpntransformcss, usedevicepoolcgpntransformcss, tkstatus_audiblealertingidle, 
            tkstatus_audiblealertingbusy, isactive, tkphoneservicedisplay, isprotected, fkmobilesmartclientprofile, tkstatus_alwaysuseprimeline, tkstatus_alwaysuseprimelineforvm, 
            hotlinedevice, fkgeolocation, fkgeolocationfilter_lp, sendgeolocation, fkvipre164transformation, usedevicepoolcgpntransformcssnatl, usedevicepoolcgpntransformcssintl, 
            usedevicepoolcgpntransformcssunkn, usedevicepoolcgpntransformcsssubs, fkfeaturecontrolpolicy, runonallnodes, enableixchannel, tkdevicetrustmode, usedevicepoolrdntransformcss, 
            fkcallingsearchspace_rdntransform, enablebfcp, requirecerlocation, usedevicepoolcgpningressdn, fkcallingsearchspace_cgpningressdn, earlyoffersupportforvoicecall, 
            enablegatewayrecordingqsig, calreference, tkcalmode, ndescription, msisdn, fkwirelesslanprofilegroup, enablecallroutingtordwhennoneisactive, 
            fkwifihotspotprofile from device d where name like '%LH-"""+postcode+"""%' and tkclass in ('253', '252')"""
        return self.sql_update(query=query)

    def createDevice_step2(self, rbimsid, ucm_location):
        query="""insert into telecastersubscribedservice (fkdevice, serviceurl, servicename, fktelecasterservice, urlbuttonindex, urllabel, secureserviceurl) select (Select pkid from device where UPPER(name) 
            like UPPER('%"""+rbimsid+"""%')), serviceurl, servicename, fktelecasterservice, urlbuttonindex, urllabel, secureserviceurl from telecastersubscribedservice 
            where fkdevice in (Select pkid from device where name like '%"""+ucm_location+"""%' and tkclass in ('253', '252'))"""
        return self.sql_update(query=query)

    def adjustAlias(self, displayname, pknummer):
        query="""update numplan set alertingname=SUBSTRING('"""+displayname+"""' FROM 1 FOR 30), alertingnameascii=SUBSTRING('"""+displayname+"""' FROM 1 FOR 30) 
            where pkid='"""+pknummer+""""'"""
        return self.sql_update(query=query)

    def assignNumber(self, pknummer, displayname, rbshortname):
        query="""insert into devicenumplanmap (fkdevice, fknumplan, numplanindex, display, displayascii, label) Select pkid, '"""+pknummer+"""', 1, SUBSTRING('"""+displayname+"""' FROM 1 FOR 30), 
            SUBSTRING('"""+displayname+"""' FROM 1 FOR 30), SUBSTRING('"""+displayname+"""' FROM 1 FOR 30) from device d where (UPPER(name) = UPPER('CSF"""+rbshortname+"""') or 
            UPPER(name) = UPPER('TAB"""+rbshortname+"""') or UPPER(name) = UPPER('BOT"""+rbshortname+"""') or UPPER(name) = UPPER('TCT"""+rbshortname+"""') or UPPER(name) like UPPER('"""+rbshortname+"""-%')) 
            and d.pkid not in (Select fkdevice from devicenumplanmap where fkdevice=d.pkid)"""
        return self.sql_update(query=query)

    def updateDescriptionOfMigratedUser(self, rbshortname):
        query="""update device set description=SUBSTRING('iManage """+rbshortname+"""' FROM 1 FOR 50) where pkid in (Select fkdevice from enduserdevicemap edm, 
            enduser e where e.pkid=edm.fkenduser and UPPER(e.userid)=UPPER('"""+rbshortname+"""'))"""
        return self.sql_update(query=query)

    def associateDevices(self, rbshortname, rbimsid):
        query="""insert into enduserdevicemap (fkdevice,fkenduser,tkuserassociation) select d.pkid, e.pkid,CASE WHEN tkclass='254' then '5' ELSE '1' END from device d,enduser e where 
            UPPER(e.userid)=UPPER('"""+rbshortname+"""') and (UPPER(d.name) = UPPER('CSF"""+rbshortname+"""') or UPPER(d.name) = UPPER('TAB"""+rbshortname+"""')  or UPPER(d.name) = UPPER('BOT"""+rbshortname+"""') or 
            UPPER(d.name) = UPPER('TCT"""+rbshortname+"""')  or UPPER(d.name) like UPPER('"""+rbshortname+"""-%'))  and d.pkid not in (select edm.fkdevice from enduserdevicemap edm,enduser e 
            where e.pkid=edm.fkenduser and UPPER(e.userid)=UPPER('"""+rbshortname+"""'))"""
        return self.sql_update(query=query)

    def setPrimaryNumber(self, pknummer, rbshortname):
        query="""insert into endusernumplanmap (fkenduser,fknumplan,tkdnusage) select pkid,'"""+pknummer+"""','1' from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""') 
            and pkid not in (select fkenduser from endusernumplanmap where tkdnusage='1')"""
        return self.sql_update(query=query)

    def assignHomeCluster(self, rbshortname):
        query = """update enduser set islocaluser='t' where UPPER(userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_update(query=query)

    def findEndUserId(self, rbshortname):
        query = """select pkid, userid from enduser where UPPER(userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_query(query=query)

    def findEndUserRbimsid(self, rbshortname):
        query = """select e.userid, cd.value from enduser e, customuserattributename cn, customuserattributedata cd where UPPER(e.userid)=UPPER('"""+rbshortname+"""') 
            and cd.fkenduser=e.pkid and cn.customfieldattributename='RBIMSID' and cn.tkcustomuserattribute=cd.tkcustomuserattribute"""
        return self.sql_query(query=query)

    def createLocalEndUser(self, rbshortname, lastname, firstname, mailid, uc_phone_number, displayname):
        query = """insert into enduser (userid*, lastname*, firstname, mailid, telephonenumber, displayname) values 
            ('"""+rbshortname+"""','"""+lastname+"""’,'"""+firstname+"""’,'"""+mailid+"""’,'"""+uc_phone_number+"""’,'"""+displayname+"""’)"""
        return self.sql_update(query=query)
    
    def insertEndUserRbimsid(self, rbimsid, rbshortname):
        query = """insert into customuserattributedata (tkcustomuserattribute, fkenduser, value) select '1',e.pkid,'"""+rbimsid+"""' from 
            enduser e where UPPER(e.userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_update(query=query)

    def insertEndUserRBOrgUnit(self, rborgunit, rbshortname):
        query="""insert into customuserattributedata (tkcustomuserattribute, fkenduser, value) select '2',e.pkid,'"""+rborgunit+"""' 
            from enduser e where UPPER(e.userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_update(query=query)

    def insertEndUserRights(self, rbshortname):
        query="""insert into enduserdirgroupmap (fkenduser,fkdirgroup) select e.pkid,dg.pkid from enduser e, dirgroup dg 
            where UPPER(e.userid)=UPPER('"""+rbshortname+"""') and dg.name='RB-Standard-EndUser-D'"""
        return self.sql_update(query=query)

    def userDetails(self, email, firstname, lastname, rbshortname):
        query = """update enduser set mailid='"""+email+"""', firstname='"""+firstname+"""', lastname='"""+lastname+"""' where UPPER(userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_update(query=query)

    def getUserInIIQScope(self):
        query= """select DISTINCT e.pkid as userpkid, e.userid, cd1.value as rbimsid, e.lastname, e.firstname, e.mailid, np.pkid as numpkid,np.dnorpattern,np.description,np.alertingname 
            from enduser e JOIN customuserattributedata cd1 ON cd1.fkenduser=e.pkid and cd1.tkcustomuserattribute='1' JOIN enduserdevicemap edm ON e.pkid=edm.fkenduser JOIN 
            device d ON d.pkid=edm.fkdevice JOIN devicenumplanmap dnmp ON d.pkid=dnmp.fkdevice JOIN numplan np ON dnmp.fknumplan=np.pkid where UPPER(np.description) like '%-iManage%'"""
        return self.sql_query(query=query)

    def getUserDetails(self, rbshortname):
        query="""select DISTINCT e.pkid as userpkid, e.userid, cd1.value as rbimsid, e.lastname, e.firstname, e.mailid, np.pkid as numpkid,np.dnorpattern,np.description,np.alertingname 
            from enduser e JOIN customuserattributedata cd1 ON cd1.fkenduser=e.pkid and cd1.tkcustomuserattribute='1' JOIN enduserdevicemap edm ON e.pkid=edm.fkenduser 
            JOIN device d ON d.pkid=edm.fkdevice JOIN devicenumplanmap dnmp ON d.pkid=dnmp.fkdevice JOIN numplan np ON dnmp.fknumplan=np.pkid 
            where UPPER(e.userid)=UPPER('"""+rbshortname+"""')"""
        return self.sql_query(query=query)


    def helperGetTKClass(self):
        query = """select d.name, d.description, d.tkclass, n.dnorpattern as DN from device as d, numplan as n, devicenumplanmap as dnpm 
                where dnpm.fkdevice = d.pkid and dnpm.fknumplan = n.pkid"""
        return self.sql_query(query = query)

    def helperGetTKClassEntries(self):
        query = """select * from device tkclass"""
        return self.sql_query(query=query)
    
    def update_phone(self, phoneName, displayname, pknummer, routePartitionName):
        try:
            return self.client.updatePhone(name=phoneName,
                                lines={"line" : {"index": 1,
                                                 "dirn": {"pattern": pknummer, "routePartitionName":routePartitionName},
                                                 "display":displayname,
                                                 "displayAscii":displayname,
                                                 "label":displayname
                                                }
                                        }
                         
                                )
        except Fault as e:
            return e

    def update_directory_number(self, pknummer, displayname, postcode, sidecode, rbshortname):
        try:
            return self.client.updateLine(pattern=pknummer, description="LH-"+postcode+"-"+sidecode+" "+rbshortname, alertingName=displayname, asciiAlertingName=displayname)
        except Fault as e:
            return e

    def update_user(self, user_id, primary_extension, routePartitionName):
        try:
            return self.client.updateUser(
                userid=user_id,
                primaryExtension={"pattern": primary_extension, "routePartitionName": routePartitionName},
            )
        except Fault as e:
            return e
