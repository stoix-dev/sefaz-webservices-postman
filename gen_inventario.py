# -*- coding: utf-8 -*-
"""Gera inventario.json com todos os webservices SEFAZ coletados.
Placeholders escritos como [[var]] e convertidos para {{var}} no final (evita
inferno de chaves). Fonte: manuais oficiais + teste real 12/09/2026."""
import json

SOAP = "http://www.w3.org/2003/05/soap-envelope"
NFE = "http://www.portalfiscal.inf.br/nfe"
CTE = "http://www.portalfiscal.inf.br/cte"
MDFE = "http://www.portalfiscal.inf.br/mdfe"


def envelope(header, body):
    h = "<soap12:Header>" + header + "</soap12:Header>\n" if header else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<soap12:Envelope xmlns:soap12="' + SOAP + '">\n'
            + h + "<soap12:Body>\n" + body + "\n</soap12:Body>\n</soap12:Envelope>")


def nwsdl(s): return "http://www.portalfiscal.inf.br/nfe/wsdl/" + s
def cwsdl(s): return "http://www.portalfiscal.inf.br/cte/wsdl/" + s
def mwsdl(s): return "http://www.portalfiscal.inf.br/mdfe/wsdl/" + s


def s(nome, metodo, action, url_h, url_p, assina, envelope_xml, obs):
    return {"nome": nome, "metodo": metodo, "soapAction": action,
            "url_homolog": url_h, "url_prod": url_p, "assinaXml": assina,
            "envelope": envelope_xml, "obs": obs}


def nota(nome, obs):
    return {"nome": nome, "metodo": "n/a", "obs": obs}


# ================= NF-e 55 =================
nfe = {"modelo": "NF-e (modelo 55)", "desc": "Webservices da NF-e 4.00. Autorizador SVRS; NFeDistribuicaoDFe e do Ambiente Nacional (RFB). SOAP 1.2. Servicos com [cadeado] exigem assinatura XMLDSig.", "servicos": [
  s("NFeStatusServico4", "nfeStatusServicoNF", nwsdl("NFeStatusServico4")+"/nfeStatusServicoNF",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx", False,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeStatusServico4")+'"><cUF>[[cUF]]</cUF><versaoDados>4.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeStatusServico4")+'"><consStatServ xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><cUF>[[cUF]]</cUF><xServ>STATUS</xServ></consStatServ></nfeDadosMsg>'),
    "Disponibilidade do autorizador. cStat 107 = em operacao."),
  s("NFeAutorizacao4 [cadeado]", "nfeAutorizacaoLote", nwsdl("NFeAutorizacao4")+"/nfeAutorizacaoLote",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx", True,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeAutorizacao4")+'"><cUF>[[cUF]]</cUF><versaoDados>4.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeAutorizacao4")+'"><enviNFe xmlns="'+NFE+'" versao="4.00"><idLote>[[idLote]]</idLote><indSinc>[[indSinc]]</indSinc><!-- NFe assinada (ref infNFe) --></enviNFe></nfeDadosMsg>'),
    "Autorizacao. indSinc=1 sincrono (recomendado), 0 assincrono. cStat 100 = autorizada."),
  s("NFeRetAutorizacao4", "nfeRetAutorizacaoLote", nwsdl("NFeRetAutorizacao4")+"/nfeRetAutorizacaoLote",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx", False,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeRetAutorizacao4")+'"><cUF>[[cUF]]</cUF><versaoDados>4.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeRetAutorizacao4")+'"><consReciNFe xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><nRec>[[nRec]]</nRec></consReciNFe></nfeDadosMsg>'),
    "Consulta recibo do lote (assincrono). cStat 104 = lote processado."),
  s("NFeConsultaProtocolo4", "nfeConsultaNF", nwsdl("NFeConsultaProtocolo4")+"/nfeConsultaNF",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx", False,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeConsultaProtocolo4")+'"><cUF>[[cUF]]</cUF><versaoDados>4.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeConsultaProtocolo4")+'"><consSitNFe xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>CONSULTAR</xServ><chNFe>[[chave44]]</chNFe></consSitNFe></nfeDadosMsg>'),
    "Situacao da NFe por chave (44 dig). Retorna protNFe e eventos."),
  s("NFeInutilizacao4 [cadeado]", "nfeInutilizacaoNF", nwsdl("NFeInutilizacao4")+"/nfeInutilizacaoNF",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/nfeinutilizacao/nfeinutilizacao4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/nfeinutilizacao/nfeinutilizacao4.asmx", True,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeInutilizacao4")+'"><cUF>[[cUF]]</cUF><versaoDados>4.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeInutilizacao4")+'"><inutNFe xmlns="'+NFE+'" versao="4.00"><infInut Id="ID[[cUF]][[ano]][[cnpj]]55[[serie]][[nNFini]][[nNFfin]]"><tpAmb>[[tpAmb]]</tpAmb><xServ>INUTILIZAR</xServ><cUF>[[cUF]]</cUF><ano>[[ano]]</ano><CNPJ>[[cnpj]]</CNPJ><mod>55</mod><serie>[[serie]]</serie><nNFIni>[[nNFini]]</nNFIni><nNFFin>[[nNFfin]]</nNFFin><xJust>[[xJust]]</xJust></infInut><!-- Signature ref infInut --></inutNFe></nfeDadosMsg>'),
    "Inutiliza faixa nao usada. Assina infInut. xJust >= 15. cStat 102 = homologada."),
  s("NFeConsultaCadastro4", "consultaCadastro4", nwsdl("CadConsultaCadastro4")+"/consultaCadastro4",
    "https://cad-homologacao.svrs.rs.gov.br/ws/cadconsultacadastro/cadconsultacadastro4.asmx",
    "https://cad.svrs.rs.gov.br/ws/cadconsultacadastro/cadconsultacadastro4.asmx", False,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("CadConsultaCadastro4")+'"><cUF>[[cUF]]</cUF><versaoDados>2.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("CadConsultaCadastro4")+'"><ConsCad xmlns="'+NFE+'" versao="2.00"><infCons><xServ>CONS-CAD</xServ><UF>[[UF]]</UF><CNPJ>[[cnpj]]</CNPJ></infCons></ConsCad></nfeDadosMsg>'),
    "Cadastro ICMS. versaoDados 2.00. Informar exatamente um: IE, CNPJ ou CPF."),
  s("NFeRecepcaoEvento4 [cadeado]", "nfeRecepcaoEvento", nwsdl("NFeRecepcaoEvento4")+"/nfeRecepcaoEvento",
    "https://nfe-homologacao.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx",
    "https://nfe.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx", True,
    envelope('<nfeCabecMsg xmlns="'+nwsdl("NFeRecepcaoEvento4")+'"><cUF>[[cUF]]</cUF><versaoDados>1.00</versaoDados></nfeCabecMsg>',
             '<nfeDadosMsg xmlns="'+nwsdl("NFeRecepcaoEvento4")+'"><envEvento xmlns="'+NFE+'" versao="1.00"><idLote>[[idLote]]</idLote><evento versao="1.00"><infEvento Id="ID[[tpEvento]][[chave44]][[nSeq]]"><cOrgao>[[cUF]]</cOrgao><tpAmb>[[tpAmb]]</tpAmb><CNPJ>[[cnpj]]</CNPJ><chNFe>[[chave44]]</chNFe><dhEvento>[[dhEvento]]</dhEvento><tpEvento>[[tpEvento]]</tpEvento><nSeqEvento>[[nSeq]]</nSeqEvento><verEvento>1.00</verEvento><detEvento versao="1.00"><!-- conteudo --></detEvento></infEvento><!-- Signature --></evento></envEvento></nfeDadosMsg>'),
    "Eventos: Cancelamento 110111, CCe 110110, Manifestacao 210200/210210/210220/210240 (recebida pelo AN). Assina cada evento."),
  s("NFeDistribuicaoDFe", "nfeDistDFeInteresse", nwsdl("NFeDistribuicaoDFe")+"/nfeDistDFeInteresse",
    "https://hom1.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx",
    "https://www1.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx", False,
    envelope("", '<nfeDistDFeInteresse xmlns="'+nwsdl("NFeDistribuicaoDFe")+'"><nfeDadosMsg><distDFeInt xmlns="'+NFE+'" versao="1.01"><tpAmb>[[tpAmb]]</tpAmb><cUFAutor>[[cUF]]</cUFAutor><CNPJ>[[cnpj]]</CNPJ><distNSU><ultNSU>[[ultNSU]]</ultNSU></distNSU></distDFeInt></nfeDadosMsg></nfeDistDFeInteresse>'),
    "Ambiente Nacional (RFB). distDFeInt COM cUFAutor, wrapper nfeDistDFeInteresse>nfeDadosMsg, SEM cabecMsg, versao 1.01. Modos: distNSU/ultNSU, consNSU/NSU, consChNFe/chNFe. Lote 50, espera 1h (656). cStat 137 vazio, 138 com docs."),
]}

# ================= NFC-e 65 =================
nfce = {"modelo": "NFC-e (modelo 65)", "desc": "NFC-e 4.00 pelo SVRS. Difere da NF-e: CSC/idCSC + QR Code (infNFeSupl), mod=65, sincrona (indSinc=1). Sem SVC; contingencia offline (tpEmis=9). SVRS atende AC/AL/AP/BA/CE/DF/ES/MA/PA/PB/PE/PI/RJ/RN/RO/RR/SC/SE/TO; AM/GO/MS/MT/PR/RS/SP proprio (URLs a confirmar).", "servicos": [
  s("NFeAutorizacao4 (NFC-e) [cadeado]", "nfeAutorizacaoLote", nwsdl("NFeAutorizacao4")+"/nfeAutorizacaoLote",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx", True,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeAutorizacao4")+'"><enviNFe xmlns="'+NFE+'" versao="4.00"><idLote>[[idLote]]</idLote><indSinc>1</indSinc><!-- NFC-e assinada com infNFeSupl (qrCode+urlChave via CSC) --></enviNFe></nfeDadosMsg>'),
    "Autorizacao NFC-e. Exige infNFeSupl (qrCode/urlChave gerados com CSC/idCSC da UF). mod=65. Sincrono."),
  s("NFeRetAutorizacao4 (NFC-e)", "nfeRetAutorizacaoLote", nwsdl("NFeRetAutorizacao4")+"/nfeRetAutorizacaoLote",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx", False,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeRetAutorizacao4")+'"><consReciNFe xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><nRec>[[nRec]]</nRec></consReciNFe></nfeDadosMsg>'),
    "So no modo assincrono. No sincrono (padrao NFC-e) o protocolo ja volta na autorizacao."),
  s("NFeStatusServico4 (NFC-e)", "nfeStatusServicoNF", nwsdl("NFeStatusServico4")+"/nfeStatusServicoNF",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx", False,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeStatusServico4")+'"><consStatServ xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><cUF>[[cUF]]</cUF><xServ>STATUS</xServ></consStatServ></nfeDadosMsg>'),
    "Disponibilidade do autorizador NFC-e."),
  s("NFeConsultaProtocolo4 (NFC-e)", "nfeConsultaNF", nwsdl("NFeConsultaProtocolo4")+"/nfeConsultaNF",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx", False,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeConsultaProtocolo4")+'"><consSitNFe xmlns="'+NFE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>CONSULTAR</xServ><chNFe>[[chave44]]</chNFe></consSitNFe></nfeDadosMsg>'),
    "Situacao da NFC-e por chave (mod 65)."),
  s("NFeRecepcaoEvento4 (NFC-e Cancelamento) [cadeado]", "nfeRecepcaoEvento", nwsdl("NFeRecepcaoEvento4")+"/nfeRecepcaoEvento",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx", True,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeRecepcaoEvento4")+'"><envEvento xmlns="'+NFE+'" versao="1.00"><idLote>[[idLote]]</idLote><!-- evento Cancelamento 110111 assinado --></envEvento></nfeDadosMsg>'),
    "Evento tipico da NFC-e e o Cancelamento (110111). CCe e Manifestacao NAO se aplicam."),
  s("NFeInutilizacao4 (NFC-e) [cadeado]", "nfeInutilizacaoNF", nwsdl("NFeInutilizacao4")+"/nfeInutilizacaoNF",
    "https://nfce-homologacao.svrs.rs.gov.br/ws/nfeinutilizacao/nfeinutilizacao4.asmx",
    "https://nfce.svrs.rs.gov.br/ws/nfeinutilizacao/nfeinutilizacao4.asmx", True,
    envelope("", '<nfeDadosMsg xmlns="'+nwsdl("NFeInutilizacao4")+'"><inutNFe xmlns="'+NFE+'" versao="4.00"><infInut Id="ID[[cUF]][[ano]][[cnpj]]65[[serie]][[nNFini]][[nNFfin]]"><tpAmb>[[tpAmb]]</tpAmb><xServ>INUTILIZAR</xServ><cUF>[[cUF]]</cUF><ano>[[ano]]</ano><CNPJ>[[cnpj]]</CNPJ><mod>65</mod><serie>[[serie]]</serie><nNFIni>[[nNFini]]</nNFIni><nNFFin>[[nNFfin]]</nNFFin><xJust>[[xJust]]</xJust></infInut></inutNFe></nfeDadosMsg>'),
    "mod=65. Inutiliza faixa nao usada. Assina infInut."),
]}

# ================= CT-e 57 =================
cte = {"modelo": "CT-e (modelo 57)", "desc": "CT-e 4.00 pelo SVRS; CTeDistribuicaoDFe do Ambiente Nacional. Autorizacao SINCRONA na 4.00 (lote assincrono descontinuado). SOAP 1.2 sem cabecMsg. Distribuicao TESTADA em 12/09/2026 (cStat 137).", "servicos": [
  s("CTeStatusServicoV4", "cteStatusServicoCT", cwsdl("CTeStatusServicoV4")+"/cteStatusServicoCT",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeStatusServicoV4/CTeStatusServicoV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeStatusServicoV4/CTeStatusServicoV4.asmx", False,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeStatusServicoV4")+'"><consStatServCte xmlns="'+CTE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>STATUS</xServ></consStatServCte></cteDadosMsg>'),
    "Disponibilidade. cStat 107 = em operacao."),
  s("CTeRecepcaoSincV4 [cadeado]", "cteRecepcao", cwsdl("CTeRecepcaoSincV4")+"/cteRecepcao",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeRecepcaoSincV4/CTeRecepcaoSincV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeRecepcaoSincV4/CTeRecepcaoSincV4.asmx", True,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeRecepcaoSincV4")+'"><CTe xmlns="'+CTE+'" versao="4.00"><!-- infCte assinada --></CTe></cteDadosMsg>'),
    "Autorizacao sincrona do CT-e 57. Assina infCte. Um doc por chamada. cStat 100 = autorizado."),
  s("CTeRecepcaoOSV4 [cadeado] (CT-e OS, mod 67)", "cteRecepcaoOS", cwsdl("CTeRecepcaoOSV4")+"/cteRecepcaoOS",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeRecepcaoOSV4/CTeRecepcaoOSV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeRecepcaoOSV4/CTeRecepcaoOSV4.asmx", True,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeRecepcaoOSV4")+'"><CTeOS xmlns="'+CTE+'" versao="4.00"><!-- infCte assinada --></CTeOS></cteDadosMsg>'),
    "CT-e Outras Prestacoes (modelo 67, raiz CTeOS)."),
  s("CTeRecepcaoGTVeV4 [cadeado] (GTV-e, mod 64)", "cteRecepcao", cwsdl("CTeRecepcaoGTVeV4")+"/cteRecepcao",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeRecepcaoGTVeV4/CTeRecepcaoGTVeV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeRecepcaoGTVeV4/CTeRecepcaoGTVeV4.asmx", True,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeRecepcaoGTVeV4")+'"><GTVe xmlns="'+CTE+'" versao="4.00"><!-- infCte assinada --></GTVe></cteDadosMsg>'),
    "Guia de Transporte de Valores (modelo 64, raiz GTVe). Metodo SOAP e cteRecepcao; distingue pelo endpoint."),
  s("CTeConsultaV4", "cteConsultaCT", cwsdl("CTeConsultaV4")+"/cteConsultaCT",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeConsultaV4/CTeConsultaV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeConsultaV4/CTeConsultaV4.asmx", False,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeConsultaV4")+'"><consSitCTe xmlns="'+CTE+'" versao="4.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>CONSULTAR</xServ><chCTe>[[chave44]]</chCTe></consSitCTe></cteDadosMsg>'),
    "Situacao do CT-e por chave (44 dig). Retorna protCTe e eventos."),
  s("CTeRecepcaoEventoV4 [cadeado]", "cteRecepcaoEvento", cwsdl("CTeRecepcaoEventoV4")+"/cteRecepcaoEvento",
    "https://cte-homologacao.svrs.rs.gov.br/ws/CTeRecepcaoEventoV4/CTeRecepcaoEventoV4.asmx",
    "https://cte.svrs.rs.gov.br/ws/CTeRecepcaoEventoV4/CTeRecepcaoEventoV4.asmx", True,
    envelope("", '<cteDadosMsg xmlns="'+cwsdl("CTeRecepcaoEventoV4")+'"><eventoCTe xmlns="'+CTE+'" versao="4.00"><infEvento Id="ID[[tpEvento]][[chave44]][[nSeq]]"><cOrgao>[[cUF]]</cOrgao><tpAmb>[[tpAmb]]</tpAmb><CNPJ>[[cnpj]]</CNPJ><chCTe>[[chave44]]</chCTe><dhEvento>[[dhEvento]]</dhEvento><tpEvento>[[tpEvento]]</tpEvento><nSeqEvento>[[nSeq]]</nSeqEvento><detEvento versaoEvento="4.00"><!-- conteudo --></detEvento></infEvento><!-- Signature --></eventoCTe></cteDadosMsg>'),
    "Eventos: CCe 110110, Cancelamento 110111, EPEC 110113, Prestacao em Desacordo 610110. Assina infEvento."),
  s("CTeDistribuicaoDFe [OK testado]", "cteDistDFeInteresse", cwsdl("CTeDistribuicaoDFe")+"/cteDistDFeInteresse",
    "https://hom1.cte.fazenda.gov.br/CTeDistribuicaoDFe/CTeDistribuicaoDFe.asmx",
    "https://www1.cte.fazenda.gov.br/CTeDistribuicaoDFe/CTeDistribuicaoDFe.asmx", False,
    envelope("", '<cteDistDFeInteresse xmlns="'+cwsdl("CTeDistribuicaoDFe")+'"><cteDadosMsg><distDFeInt xmlns="'+CTE+'" versao="1.00"><tpAmb>[[tpAmb]]</tpAmb><cUFAutor>[[cUF]]</cUFAutor><CNPJ>[[cnpj]]</CNPJ><distNSU><ultNSU>[[ultNSU]]</ultNSU></distNSU></distDFeInt></cteDadosMsg></cteDistDFeInteresse>'),
    "TESTADO 12/09/2026 (cStat 137). Ambiente Nacional. distDFeInt COM cUFAutor, wrapper cteDistDFeInteresse>cteDadosMsg, SEM cabecMsg, versao 1.00. Modos: distNSU/ultNSU, consNSU/NSU, consChNSU/chCTe. Lote 50, espera 1h (656)."),
  nota("CTeInutilizacao", "O CT-e 4.00 NAO oferece inutilizacao de numeracao no rol nacional (diferente da NF-e)."),
  nota("CTeRecepcao/CTeRetRecepcao (lote assincrono)", "DESCONTINUADO na 4.00. Autorizacao e exclusivamente sincrona (SincV4/OSV4/GTVeV4). Existe tambem CTeRecepcaoSimpV4 (CT-e Simplificado)."),
]}

# ================= MDF-e 58 =================
mdfe = {"modelo": "MDF-e (modelo 58)", "desc": "MDF-e 3.00 pelo SVRS (atende quase todas as UFs, inclusive SP); distribuicao tambem no SVRS. Autorizacao SINCRONA (dados em GZip+base64). SOAP 1.2. cabecMsg opcional na 3.00, exceto na distribuicao (cUF no header, confirmado por teste). Distribuicao TESTADA 12/09/2026 (cStat 137).", "servicos": [
  s("MDFeStatusServico", "mdfeStatusServicoMDF", mwsdl("MDFeStatusServico")+"/mdfeStatusServicoMDF",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeStatusServico/MDFeStatusServico.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeStatusServico/MDFeStatusServico.asmx", False,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeStatusServico")+'"><cUF>[[cUF]]</cUF><versaoDados>3.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeStatusServico")+'"><consStatServMDFe xmlns="'+MDFE+'" versao="3.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>STATUS</xServ></consStatServMDFe></mdfeDadosMsg>'),
    "Disponibilidade. cStat 107 = em operacao."),
  s("MDFeRecepcaoSinc [cadeado]", "mdfeRecepcao", mwsdl("MDFeRecepcaoSinc")+"/mdfeRecepcao",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeRecepcaoSinc/MDFeRecepcaoSinc.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeRecepcaoSinc/MDFeRecepcaoSinc.asmx", True,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeRecepcaoSinc")+'"><cUF>[[cUF]]</cUF><versaoDados>3.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeRecepcaoSinc")+'">[[MDFe_gzip_base64]]</mdfeDadosMsg>'),
    "Autorizacao sincrona 3.00. Area de dados COMPACTADA (GZip -> base64). Assina infMDFe. cStat 100 = autorizado."),
  s("MDFeConsulta", "mdfeConsultaMDF", mwsdl("MDFeConsulta")+"/mdfeConsultaMDF",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeConsulta/MDFeConsulta.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeConsulta/MDFeConsulta.asmx", False,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeConsulta")+'"><cUF>[[cUF]]</cUF><versaoDados>3.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeConsulta")+'"><consSitMDFe xmlns="'+MDFE+'" versao="3.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>CONSULTAR</xServ><chMDFe>[[chave44]]</chMDFe></consSitMDFe></mdfeDadosMsg>'),
    "Situacao do MDF-e por chave (44 dig)."),
  s("MDFeConsNaoEnc", "mdfeConsNaoEnc", mwsdl("MDFeConsNaoEnc")+"/mdfeConsNaoEnc",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeConsNaoEnc/MDFeConsNaoEnc.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeConsNaoEnc/MDFeConsNaoEnc.asmx", False,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeConsNaoEnc")+'"><cUF>[[cUF]]</cUF><versaoDados>3.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeConsNaoEnc")+'"><consMDFeNaoEnc xmlns="'+MDFE+'" versao="3.00"><tpAmb>[[tpAmb]]</tpAmb><xServ>CONSULTAR NAO ENCERRADOS</xServ><CNPJ>[[cnpj]]</CNPJ></consMDFeNaoEnc></mdfeDadosMsg>'),
    "MDF-e nao encerrados do emitente. xServ literal 'CONSULTAR NAO ENCERRADOS'."),
  s("MDFeRecepcaoEvento [cadeado]", "mdfeRecepcaoEvento", mwsdl("MDFeRecepcaoEvento")+"/mdfeRecepcaoEvento",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeRecepcaoEvento/MDFeRecepcaoEvento.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeRecepcaoEvento/MDFeRecepcaoEvento.asmx", True,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeRecepcaoEvento")+'"><cUF>[[cUF]]</cUF><versaoDados>3.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeRecepcaoEvento")+'"><eventoMDFe xmlns="'+MDFE+'" versao="3.00"><infEvento Id="ID[[tpEvento]][[chave44]][[nSeq]]"><cOrgao>[[cUF]]</cOrgao><tpAmb>[[tpAmb]]</tpAmb><CNPJ>[[cnpj]]</CNPJ><chMDFe>[[chave44]]</chMDFe><dhEvento>[[dhEvento]]</dhEvento><tpEvento>[[tpEvento]]</tpEvento><nSeqEvento>[[nSeq]]</nSeqEvento><detEvento versaoEvento="3.00"><!-- conteudo --></detEvento></infEvento><!-- Signature --></eventoMDFe></mdfeDadosMsg>'),
    "Eventos: Cancelamento 110111, Encerramento 110112, Inclusao de Condutor 110114, Inclusao de DF-e 110115, Pagamento 110116. Assina infEvento."),
  s("MDFeDistribuicaoDFe [OK testado]", "mdfeDistDFeInteresse", mwsdl("MDFeDistribuicaoDFe")+"/mdfeDistDFeInteresse",
    "https://mdfe-homologacao.svrs.rs.gov.br/ws/MDFeDistribuicaoDFe/MDFeDistribuicaoDFe.asmx",
    "https://mdfe.svrs.rs.gov.br/ws/MDFeDistribuicaoDFe/MDFeDistribuicaoDFe.asmx", False,
    envelope('<mdfeCabecMsg xmlns="'+mwsdl("MDFeDistribuicaoDFe")+'"><cUF>[[cUF]]</cUF><versaoDados>1.00</versaoDados></mdfeCabecMsg>',
             '<mdfeDadosMsg xmlns="'+mwsdl("MDFeDistribuicaoDFe")+'"><distDFeInt xmlns="'+MDFE+'" versao="1.00"><tpAmb>[[tpAmb]]</tpAmb><CNPJ>[[cnpj]]</CNPJ><distNSU><ultNSU>[[ultNSU]]</ultNSU></distNSU></distDFeInt></mdfeDadosMsg>'),
    "TESTADO 12/09/2026 (cStat 137). distDFeInt SEM cUFAutor (cUF vai no mdfeCabecMsg do header), mdfeDadosMsg DIRETO no Body (sem wrapper). Suporta APENAS distNSU e consNSU (NAO tem consChNSU)."),
]}

eventos = [
  {"tpEvento": "110110", "nome": "Carta de Correcao (CC-e)", "modelo": "NF-e, CT-e", "obs": "Nao se aplica a NFC-e."},
  {"tpEvento": "110111", "nome": "Cancelamento", "modelo": "NF-e, NFC-e, CT-e, MDF-e", "obs": "Exige nProt e xJust >= 15."},
  {"tpEvento": "110112", "nome": "Cancel. por Substituicao (NF-e) / Encerramento (MDF-e)", "modelo": "NF-e, MDF-e", "obs": "Mesmo codigo, significado por modelo."},
  {"tpEvento": "110113", "nome": "EPEC (CT-e)", "modelo": "CT-e", "obs": ""},
  {"tpEvento": "110114", "nome": "Inclusao de Condutor", "modelo": "MDF-e", "obs": ""},
  {"tpEvento": "110115", "nome": "Inclusao de DF-e", "modelo": "MDF-e", "obs": ""},
  {"tpEvento": "110116", "nome": "Pagamento Operacao Transporte", "modelo": "MDF-e", "obs": ""},
  {"tpEvento": "110140", "nome": "EPEC (NF-e)", "modelo": "NF-e", "obs": "Ao SVC-AN. NFC-e usa offline (tpEmis=9)."},
  {"tpEvento": "210200/210210/210220/210240", "nome": "Manifestacao do Destinatario", "modelo": "NF-e", "obs": "Recebido pelo AN. Nao existe para NFC-e."},
  {"tpEvento": "610110/610111", "nome": "Prestacao de Servico em Desacordo", "modelo": "CT-e", "obs": "Registrado pelo tomador."},
]

variaveis = [
  {"key": "url", "value": "", "description": "URL do servico (homolog ou prod), copiada da descricao da request."},
  {"key": "tpAmb", "value": "2", "description": "1=producao, 2=homologacao"},
  {"key": "cUF", "value": "42", "description": "codigo IBGE da UF (42=SC, 35=SP, 43=RS)"},
  {"key": "UF", "value": "SC", "description": "sigla da UF (consulta cadastro)"},
  {"key": "cnpj", "value": "", "description": "CNPJ do autor/emitente, sem pontuacao"},
  {"key": "chave44", "value": "", "description": "chave de acesso de 44 digitos"},
  {"key": "ultNSU", "value": "000000000000000", "description": "distribuicao: ultimo NSU (0 = primeira carga)"},
  {"key": "nRec", "value": "", "description": "recibo do lote (retorno assincrono)"},
  {"key": "idLote", "value": "1", "description": "identificador do lote"},
  {"key": "indSinc", "value": "1", "description": "1=sincrono, 0=assincrono"},
  {"key": "tpEvento", "value": "110111", "description": "codigo do evento (ver pasta Eventos)"},
  {"key": "nSeq", "value": "1", "description": "sequencia do evento"},
  {"key": "ano", "value": "26", "description": "ano (2 digitos) para inutilizacao"},
  {"key": "serie", "value": "1", "description": "serie do documento"},
  {"key": "nNFini", "value": "1", "description": "numero inicial (inutilizacao)"},
  {"key": "nNFfin", "value": "1", "description": "numero final (inutilizacao)"},
  {"key": "xJust", "value": "", "description": "justificativa (min 15 caracteres)"},
  {"key": "dhEvento", "value": "", "description": "data/hora do evento (ISO com fuso)"},
]

descricao = (
  "Catalogo completo dos webservices da SEFAZ: NF-e (55), NFC-e (65), CT-e (57) e MDF-e (58). "
  "Uma pasta por modelo, cada request com envelope SOAP 1.2 pronto e variaveis {{}}.\n\n"
  "## Como usar\n"
  "1. Escolha a request. Copie a URL (homolog ou prod) da descricao para a variavel {{url}}.\n"
  "2. Certificado e-CNPJ A1: Settings > Certificates > Add Certificate, por host, com o .pfx e senha. "
  "Desligue a verificacao SSL do servidor (ACs da ICP-Brasil nao estao no trust store do Postman).\n"
  "3. Ajuste as variaveis (cnpj, cUF, tpAmb, chave44...) e dispare.\n\n"
  "## Convencoes\n"
  "- [cadeado] no nome = o XML de dados exige assinatura XMLDSig (autorizacao, eventos, inutilizacao). "
  "O Postman nao assina XML; para esses use a POC em codigo ou um assinador. Consultas e distribuicao nao assinam.\n"
  "- [OK testado] = validado contra a SEFAZ em 12/09/2026 (cStat 137).\n"
  "- Todos SOAP 1.2: o action vai no Content-Type, nao em header SOAPAction separado.\n\n"
  "## Autorizadores\n"
  "URLs default do SVRS. NFeDistribuicaoDFe e CTeDistribuicaoDFe sao do Ambiente Nacional (RFB). "
  "NFC-e em AM/GO/MS/MT/PR/RS/SP usa ambiente proprio (URLs a confirmar). Contingencia NF-e: SVC-AN/SVC-RS; NFC-e: offline (tpEmis=9).\n\n"
  "Ref: Manuais NF-e/NFC-e 4.00, CT-e 4.00, MDF-e 3.00b, NT 2015.002."
)

out = {"descricao": descricao, "variaveis": variaveis,
       "modelos": [nfe, nfce, cte, mdfe], "eventos": eventos}
data = json.dumps(out, ensure_ascii=False, indent=2).replace("[[", "{{").replace("]]", "}}")
open("inventario.json", "w", encoding="utf-8").write(data)
print("inventario.json gerado")
