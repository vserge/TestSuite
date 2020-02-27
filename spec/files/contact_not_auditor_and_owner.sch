<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
  <ns prefix="auc" uri="http://buildingsync.net/schemas/bedes-auc/2019"/>
  <include href="../../lib/contactElements.sch#con.notAuditorAndOwner"/>
  <phase id="Tests">
    <active pattern="con.con.notAuditorAndOwner"/>
  </phase>

  <pattern id="con.con.notAuditorAndOwner" is-a="con.notAuditorAndOwner">
    <param name="parent" value="auc:Facility/auc:Contacts/auc:Contact"/>
  </pattern>
</schema>