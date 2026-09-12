# Catálogo de Webservices da SEFAZ (coleção Postman)

Coleção Postman completa e documentada dos webservices dos documentos fiscais
eletrônicos brasileiros: **NF-e (55), NFC-e (65), CT-e (57) e MDF-e (58)**.

Arquivo: `postman/SEFAZ-Webservices-Catalogo.postman_collection.json`
(29 itens em 5 pastas: uma por modelo + referência de eventos.)

## Por que existe

Integrar com a SEFAZ exige garimpar manuais (MOC NF-e/NFC-e 4.00, CT-e 4.00,
MDF-e 3.00b, NT 2015.002) e portais de autorizadores para descobrir URL,
envelope SOAP e peculiaridades de cada serviço. Esta coleção entrega isso
pronto: cada request com envelope SOAP 1.2 montado e variáveis `{{}}`.

Os dois serviços de distribuição DFe (CT-e e MDF-e) foram **validados contra a
SEFAZ em produção em 12/09/2026** (cStat 137) e estão marcados com `[OK testado]`.

## Setup no Postman

1. **Import** > `postman/SEFAZ-Webservices-Catalogo.postman_collection.json`.
2. **Certificado** (Settings > Certificates > Add Certificate): adicione seu e-CNPJ A1
   (`.pfx` + senha) por host. Para as distribuições:
   `www1.cte.fazenda.gov.br`, `mdfe.svrs.rs.gov.br`, `mdfe-homologacao.svrs.rs.gov.br`.
3. **Settings > General**: desligue "SSL certificate verification" (as ACs da
   ICP-Brasil não estão no trust store do Postman).
4. Em cada request, copie a URL (homolog ou prod, da descrição) para a variável
   `{{url}}`, ajuste `cnpj`, `cUF`, `tpAmb` etc, e dispare.

## Convenções

- `[cadeado]` no nome: o XML de dados exige **assinatura XMLDSig** (autorização,
  eventos, inutilização). O Postman não assina XML; para esses serviços use um
  assinador ou código próprio. Consultas, status e distribuição **não** assinam.
- `[OK testado]`: validado contra a SEFAZ (cStat 137).
- Todos SOAP 1.2: o `action` viaja no `Content-Type`, não em header `SOAPAction`.

## Diferenças que pegam (aprendidas no teste real)

- **CT-e distribuição** (Ambiente Nacional): `distDFeInt` COM `cUFAutor`, wrapper
  `cteDistDFeInteresse > cteDadosMsg`, sem cabecMsg.
- **MDF-e distribuição** (SVRS): `distDFeInt` SEM `cUFAutor` (o `cUF` vai no
  `mdfeCabecMsg` do header), `mdfeDadosMsg` direto no Body. Só tem `distNSU` e
  `consNSU` (não tem `consChNSU`).
- **NF-e distribuição** (AN): igual ao CT-e (com `cUFAutor`), versão 1.01.
- **CT-e 4.00**: autorização é só síncrona (SincV4/OSV4/GTVeV4); lote assíncrono
  e inutilização não existem no rol nacional.
- **MDF-e 3.00**: autorização síncrona com área de dados em GZip+base64.
- **NFC-e**: exige CSC + QR Code (infNFeSupl); sem SVC (contingência offline
  tpEmis=9); UFs AM/GO/MS/MT/PR/RS/SP têm ambiente próprio.

## Escopo e limites

- URLs default do **SVRS** (atende a maioria das UFs) + **Ambiente Nacional**
  para as distribuições. Não cobre as 27 UFs uma a uma; para autorizador próprio
  (ex. NFC-e SP), trocar a URL na variável.
- Eventos estão como pasta de referência (códigos de `tpEvento`); são enviados
  pelo `RecepcaoEvento` do respectivo modelo.

## Como é gerado

Fonte de verdade: `gen_inventario.py` gera `inventario.json`; `build_collection.py`
monta o `.json` do Postman. Para propor mudança, edite o `gen_inventario.py`,
rode os dois e abra um PR.

## Repositórios irmãos

- [ciot-integradoras-postman](https://github.com/stoix-dev/ciot-integradoras-postman): CIOT via ANTT (pefServices) e integradoras de pagamento de frete
- [antt-webservices-postman](https://github.com/stoix-dev/antt-webservices-postman): webservices da ANTT (CIOT, RNTRC, dados abertos)

## Sobre

Mantido pela [Stoix](https://stoix.dev). Licença MIT.
