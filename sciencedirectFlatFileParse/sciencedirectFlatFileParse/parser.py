import pandas as pd
from lxml import etree

class SD_FF_parse:
    def __init__(self):
        self.namespaces = {
            '': 'http://www.elsevier.com/xml/ja/dtd',
            'xocs': 'http://www.elsevier.com/xml/xocs/dtd',
            'ce': 'http://www.elsevier.com/xml/common/dtd',
            'ja': 'http://www.elsevier.com/xml/ja/dtd',
            'cals': 'http://www.elsevier.com/xml/common/cals/dtd',
            'mml': 'http://www.w3.org/1998/Math/MathML',
            'sb': 'http://www.elsevier.com/xml/common/struct-bib/dtd',
            'tb': 'http://www.elsevier.com/xml/common/table/dtd',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xs': 'http://www.w3.org/2001/XMLSchema',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    def get_xmlType(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        itemweight = root.find('.//xocs:item-weight', self.namespaces)
        return itemweight.text

    def Meta_parse_Normalize_FIRSTAuthors(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse author information and return as DataFrame"""
        authors = []
        
        # In this XML, author info is in normalized form
        surname = root.find('.//xocs:normalized-first-auth-surname', namespaces=self.namespaces)
        initials = root.find('.//xocs:normalized-first-auth-initial', namespaces=self.namespaces)
        
        if surname is not None and initials is not None:
            authors.append({
                'surname': surname.text,
                'initials': initials.text
            })
        
        # Add logic to parse additional authors if present in the XML
        return pd.DataFrame(authors)
    
    def Meta_parse_references(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse references and return as DataFrame"""
        references = []
        
        for ref in root.findall('.//xocs:ref-info', namespaces=self.namespaces):
            ref_dict = {
                'refid': ref.get('refid', ''),
                'surname': ref.findtext('xocs:ref-normalized-surname', default='', namespaces=self.namespaces),
                'initials': ref.findtext('xocs:ref-normalized-initial', default='', namespaces=self.namespaces),
                'pub_year': ref.findtext('xocs:ref-pub-year', default='', namespaces=self.namespaces),
                'first_page': ref.findtext('xocs:ref-first-fp', default=None, namespaces=self.namespaces),
                'last_page': ref.findtext('xocs:ref-last-lp', default=None, namespaces=self.namespaces),
                'article_number': ref.findtext('xocs:ref-article-number', default=None, namespaces=self.namespaces)
            }
            if ref_dict['article_number'] is not None:
                ref_dict['article_number'] = ref_dict['article_number'].strip()
            references.append(ref_dict)
        
        return pd.DataFrame(references)
    
    def Meta_parse_attachments(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse attachments and return as DataFrame"""
        attachments = []
        
        for attach in root.findall('.//xocs:attachment', namespaces=self.namespaces):
            attach_dict = {
                'eid': attach.findtext('xocs:attachment-eid', default='', namespaces=self.namespaces),
                'url': attach.findtext('xocs:ucs-locator', default='', namespaces=self.namespaces),
                'filename': attach.findtext('xocs:filename', default='', namespaces=self.namespaces),
                'filetype': attach.findtext('xocs:extension', default='', namespaces=self.namespaces),
                'filesize': int(attach.findtext('xocs:filesize', default='0', namespaces=self.namespaces)),
                'attachment_type': attach.findtext('xocs:attachment-type', default='', namespaces=self.namespaces)
            }
            attachments.append(attach_dict)
        
        return pd.DataFrame(attachments)
    
    def Meta_parse_webpdf(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse attachments and return as DataFrame"""
        webpdf = []

        webpdfall = root.find('.//xocs:web-pdf', namespaces=self.namespaces)
        webpdf_dict = {
            'eid': webpdfall.findtext('xocs:attachment-eid', default='', namespaces=self.namespaces),
            'url': webpdfall.findtext('xocs:ucs-locator', default='', namespaces=self.namespaces),
            'filename': webpdfall.findtext('xocs:filename', default='', namespaces=self.namespaces),
            'filetype': webpdfall.findtext('xocs:extension', default='', namespaces=self.namespaces),
            'filesize': int(webpdfall.findtext('xocs:filesize', default='0', namespaces=self.namespaces)),
            
        }
        
        webpdf.append(webpdf_dict)
        
        return pd.DataFrame(webpdf)

    def Meta_parse_webpdfimg(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse attachments and return as DataFrame"""
        webpdfimg = []

        webpdfimageall = root.find('.//xocs:web-pdf-image', namespaces=self.namespaces)
        webpdfimage_dict = {
            'eid': webpdfimageall.findtext('xocs:attachment-eid', default='', namespaces=self.namespaces),
            'url': webpdfimageall.findtext('xocs:ucs-locator', default='', namespaces=self.namespaces),
            'filename': webpdfimageall.findtext('xocs:filename', default='', namespaces=self.namespaces),
            'filetype': webpdfimageall.findtext('xocs:extension', default='', namespaces=self.namespaces),
            'filesize': int(webpdfimageall.findtext('xocs:filesize', default='0', namespaces=self.namespaces)),
            
        }
        
        webpdfimg.append(webpdfimage_dict)
        
        return pd.DataFrame(webpdfimg)

    def Meta_parse_funding(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse funding information and return as DataFrame"""
        funding_list = []
        
        for fund in root.findall('.//xocs:funding', namespaces=self.namespaces):
            agency = fund.find('xocs:funding-agency', namespaces=self.namespaces)
            if agency is None:
                agency = fund.find('xocs:funding-agency-matched-string', namespaces=self.namespaces)
            
            fund_dict = {
                'agency': agency.text if agency is not None else '',
                'funding_id': fund.findtext('xocs:funding-id', default=None, namespaces=self.namespaces),
                'agency_acronym': fund.findtext('xocs:funding-agency-acronym', default=None, namespaces=self.namespaces),
                'funding-agency': fund.findtext('xocs:funding-agency', default=None, namespaces=self.namespaces),
                'funding-agency-id': fund.findtext('xocs:funding-agency-id', default=None, namespaces=self.namespaces),
                'funding-agency-country': fund.findtext('xocs:funding-agency-country', default=None, namespaces=self.namespaces),

            }
            funding_list.append(fund_dict)
        
        return pd.DataFrame(funding_list)
    
    def Meta_parse_sections_title(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse article sections and return as DataFrame"""
        sections = []
        
        for toc_entry in root.findall('.//xocs:item-toc-entry[@ref-elem="ce:sections"]', namespaces=self.namespaces):
            label = toc_entry.find('xocs:item-toc-label', namespaces=self.namespaces)
            title = toc_entry.find('xocs:item-toc-section-title', namespaces=self.namespaces)
            
            
            if label is not None:
                label_text = label.text
            else:
                label_text = ''

            if title is not None:
                title_text = title.text
            else:
                title_text = '' 

            sections.append({
                'section_label': label_text,
                'section_title': title_text
            })
    
        return pd.DataFrame(sections)
    
    def Meta_parse_article_metadata(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse main article metadata and return as DataFrame"""
        metadata = {}
        
        # Basic metadata
        metadata['title'] = root.findtext('.//xocs:normalized-article-title', default='', namespaces=self.namespaces)
        metadata['journal_title'] = root.findtext('.//xocs:srctitle', default='', namespaces=self.namespaces)
        metadata['issn'] = root.findtext('.//xocs:issn-primary-formatted', default='', namespaces=self.namespaces)
        metadata['volume'] = root.findtext('.//xocs:vol-first', default='', namespaces=self.namespaces)
        metadata['issue'] = root.findtext('.//xocs:iss-first', default='', namespaces=self.namespaces)
        metadata['first_page'] = root.findtext('.//xocs:first-page', default='', namespaces=self.namespaces)
        metadata['last_page'] = root.findtext('.//xocs:last-page', default='', namespaces=self.namespaces)
        metadata['publication_date'] = root.findtext('.//xocs:cover-date-text', default='', namespaces=self.namespaces)
        metadata['doi'] = root.findtext('.//xocs:doi', default='', namespaces=self.namespaces)
        metadata['pii'] = root.findtext('.//xocs:pii-formatted', default='', namespaces=self.namespaces)
        metadata['eid'] = root.findtext('.//xocs:eid', default='', namespaces=self.namespaces)
        metadata['documentType'] = root.findtext('.//xocs:document-type', default='', namespaces=self.namespaces)
        metadata['documentSubType'] = root.findtext('.//xocs:document-subtype', default='', namespaces=self.namespaces)

        # Open access status
        oa_status = root.find('.//xocs:oa-article-status', namespaces=self.namespaces)
        metadata['is_open_access'] = oa_status.get('is-open-access', '0') == '1' if oa_status is not None else False
        
        # License information
        license_line = root.find('.//xocs:cp-license-line[@lang="en"]', namespaces=self.namespaces)
        metadata['license'] = license_line.text if license_line is not None else ''
        
        # Create DataFrame from single row
        return pd.DataFrame([metadata])
    
    def SerialItem_parse_Coredata(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse basic article metadata"""
        coredata = {}
        
        # Journal and article info
        item_info = root.find('.//item-info', self.namespaces)
        if item_info is not None:
            coredata['journal_id'] = item_info.find('jid', self.namespaces).text if item_info.find('jid', self.namespaces) is not None else None
            coredata['article_id'] = item_info.find('aid', self.namespaces).text if item_info.find('aid', self.namespaces) is not None else None
            coredata['doi'] = item_info.find('ce:doi', self.namespaces).text if item_info.find('ce:doi', self.namespaces) is not None else None
            coredata['pii'] = item_info.find('ce:pii', self.namespaces).text if item_info.find('ce:pii', self.namespaces) is not None else None
            coredata['copyright'] = item_info.find('ce:copyright', self.namespaces).text if item_info.find('ce:copyright', self.namespaces) is not None else None
        
        # Title
        title = root.find('.//ce:title', self.namespaces)
        coredata['title'] = ''.join(title.itertext()) if title is not None else None
        
        # Abstract
        # Abstract

        ABSTRACT_COLUMNS = {
            "graphical": "graphical_abstract",
            "author-highlights": "author_highlights",
            "author": "author_abstract"
        }
        abstractdata = {col: None for col in ABSTRACT_COLUMNS.values()}  # 初始化所有列为 None
        abstracts = root.findall('.//ce:abstract', self.namespaces)

        for abstract in abstracts:
            abstract_class = abstract.get("class")
            
            # 处理图形摘要（class="graphical"）
            if abstract_class == "graphical":
                # 查找图形摘要中的链接（ce:figure -> ce:link）
                link = abstract.find('.//ce:figure/ce:link', self.namespaces)
                if link is not None:
                    href = link.get(f"{{{self.namespaces['xlink']}}}href")  # 获取 xlink:href 属性
                    abstractdata["graphical_abstract"] = href
            
            # 处理其他类型（如 author-highlights 和 author）
            elif abstract_class in ["author-highlights", "author"]:
                # 提取文本内容（原有逻辑）
                abstract_text = []
                abstract_secs = abstract.findall('.//ce:abstract-sec', self.namespaces)
                for sec in abstract_secs:
                    simple_paras = sec.findall('.//ce:simple-para', self.namespaces)
                    for para in simple_paras:
                        text = ''.join(para.itertext()).strip()
                        if text:
                            abstract_text.append(text)
                # 存储到对应字段
                target_field = "author_highlights" if abstract_class == "author-highlights" else "author_abstract"
                abstractdata[target_field] = ' '.join(abstract_text) if abstract_text else None



        # Keywords
        keywords = root.find('.//ce:keywords', self.namespaces)
        if keywords is not None:
            coredata['keywords'] = " ; ".join([kw.xpath("string()") for kw in keywords.findall('ce:keyword/ce:text', self.namespaces)])
        coredata['graphical_abstract'] = abstractdata['graphical_abstract']
        coredata['author_highlights'] = abstractdata['author_highlights']
        coredata['author_abstract'] = abstractdata['author_abstract']
        return pd.DataFrame([coredata])
    
    def SerialItem_parse_rawtext(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        raw_text_dict = {}
        """Parse basic article metadata"""
        rawtext_element = root.find('.//xocs:rawtext', self.namespaces)
        raw_text = rawtext_element.text if rawtext_element is not None else None
        if raw_text is None:
            return pd.DataFrame()
        else:

            raw_text_dict = {

                "raw_text": raw_text
                
            }
            return pd.DataFrame([raw_text_dict])

    def SerialItem_parse_authors(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse author information"""
        authors = []
        author_group = root.find('.//ce:author-group', self.namespaces)
        
        if author_group is not None:
            for author in author_group.findall('ce:author', self.namespaces):
                author_data = {
                    'given_name': author.find('ce:given-name', self.namespaces).text if author.find('ce:given-name', self.namespaces) is not None else None,
                    'surname': author.find('ce:surname', self.namespaces).text if author.find('ce:surname', self.namespaces) is not None else None,
                    'email': author.find('ce:e-address', self.namespaces).text if author.find('ce:e-address', self.namespaces) is not None else None,
                    'affiliations': []
                }
                
                # Get affiliation references
                for ref in author.findall('ce:cross-ref', self.namespaces):
                    if 'refid' in ref.attrib:
                        aff_id = ref.attrib['refid']
                        affiliation = author_group.find(f'ce:affiliation[@id="{aff_id}"]', self.namespaces)
                        if affiliation is not None:
                            author_data['affiliations'].append(affiliation.find('ce:textfn', self.namespaces).text)
                
                authors.append(author_data)
        
        return pd.DataFrame(authors)
    
    def SerialItem_parse_figures(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse figures and their captions"""
        figures = []
        
        # Find all figure elements
        for figure in root.findall('.//ce:figure', self.namespaces):
            fig_data = {
                'id': figure.get('id'),
                'label': None,
                'caption': None,
                'link': None
            }
            
            # Get figure label
            label = figure.find('ce:label', self.namespaces)
            if label is not None:
                fig_data['label'] = label.text
            
            # Get figure caption
            caption = figure.find('ce:caption', self.namespaces)
            if caption is not None:
                # Extract all text content including nested elements
                caption_text = []
                for elem in caption.iter():
                    if elem.tag == f"{{{self.namespaces['ce']}}}simple-para":
                        # Handle the main paragraph
                        if elem.text:
                            caption_text.append(elem.text)
                        # Handle all child elements
                        for child in elem:
                            if child.tag == f"{{{self.namespaces['ce']}}}italic":
                                # Preserve italic formatting
                                caption_text.append(f"<i>{child.text}</i>")
                                if child.tail:
                                    caption_text.append(child.tail)
                            else:
                                # For other elements, just get the text
                                if child.text:
                                    caption_text.append(child.text)
                                if child.tail:
                                    caption_text.append(child.tail)
                    elif elem.tag != caption.tag:  # Skip the caption element itself
                        if elem.text:
                            caption_text.append(elem.text)
                        if elem.tail:
                            caption_text.append(elem.tail)
                
                # Join all parts and clean up whitespace
                fig_data['caption'] = ' '.join(''.join(caption_text).split())
            
            # Get figure link
            link = figure.find('ce:link', self.namespaces)
            if link is not None:
                fig_data['link'] = figure.find('ce:link', self.namespaces).attrib.get('{http://www.w3.org/1999/xlink}href')
            
            figures.append(fig_data)
        
        return pd.DataFrame(figures)
    
    def SerialItem_parse_tables(self, xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse tables from the XML document with improved caption handling"""
        tables = []
        
        # Define additional namespaces needed for table parsing
        table_ns = {
            'cals': 'http://www.elsevier.com/xml/common/cals/dtd',
            'ce': 'http://www.elsevier.com/xml/common/dtd'
        }
        
        for table in root.findall('.//ce:table', self.namespaces):
            table_data = {
                'id': table.get('id'),
                'label': None,
                'caption': [],
                'headers': [],
                'rows': []
            }
            
            # Get table label (e.g., "Table 1")
            label = table.find('ce:label', self.namespaces)
            if label is not None:
                table_data['label'] = label.text
                
            # Get table caption (may span multiple lines)
            caption = table.find('ce:caption', self.namespaces)
            if caption is not None:
                for para in caption.findall('.//ce:simple-para', self.namespaces):
                    if para.text:
                        table_data['caption'].append(para.text.strip())
                    # Handle mixed content (text and elements)
                    caption_text = ''.join(para.itertext()).strip()
                    if caption_text:
                        table_data['caption'].append(caption_text)
                # Remove duplicates and join with spaces
                table_data['caption'] = ' '.join(list(dict.fromkeys(table_data['caption'])))
            
            # Parse table structure - using the cals namespace
            tgroup = table.find('cals:tgroup', table_ns)
            
            if tgroup is not None:
                # Get column specifications
                cols = tgroup.findall('cals:colspec', table_ns)
                num_cols = len(cols) if cols else 0
                
                # Parse headers
                thead = tgroup.find('cals:thead', table_ns)
                
                if thead is not None:
                    for row in thead.findall('cals:row', table_ns):
                        
                        header_row = []
                        for entry in row.findall('ce:entry', table_ns):
                            
                            # Handle entry content which might contain formatting
                            text = ''.join(entry.itertext()).strip()
                            header_row.append(text)
                        table_data['headers'].append(header_row)
                
                # Parse body rows
                tbody = tgroup.find('cals:tbody', table_ns)
                if tbody is not None:
                    for row in tbody.findall('cals:row', table_ns):
                        data_row = []
                        for entry in row.findall('ce:entry', table_ns):
                            # Handle entry content which might contain italic elements etc.
                            text = ''.join(entry.itertext()).strip()
                            data_row.append(text)
                        table_data['rows'].append(data_row)
            
            tables.append(table_data)
        return tables
    
    def SerialItem_parse_sections(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse all sections and subsections from the XML document"""
        sections = []
        
        if len(root.findall('.//ce:section', self.namespaces)) >0:
            # Find all top-level sections
            for section in root.findall('.//ce:section', self.namespaces):
                section_data = {
                    'id': section.get('id'),
                    'label': section.find('ce:label', self.namespaces).text if section.find('ce:label', self.namespaces) is not None else None,
                    'title': section.find('ce:section-title', self.namespaces).text if section.find('ce:section-title', self.namespaces) is not None else None,
                    'paragraphs': [],
                    'subsections': []
                }
                
                # Process all paragraphs in this section
                for para in section.findall('ce:para', self.namespaces):
                    para_text = []
                    # Handle mixed content (text and elements) within paragraphs
                    for elem in para.iter():
                        if elem.text and elem.text.strip():
                            para_text.append(elem.text.strip())
                        if elem.tag == f"{{{self.namespaces['ce']}}}cross-ref":
                            ref_text = ''.join(elem.itertext()).strip()
                            para_text.append(f"[{ref_text}]")
                        if elem.tail and elem.tail.strip():
                            para_text.append(elem.tail.strip())
                    
                    section_data['paragraphs'].append(' '.join(para_text))
                
                # Process subsections recursively
                for subsection in section.findall('ce:section', self.namespaces):
                    subsection_data = {
                        'id': subsection.get('id'),
                        'label': subsection.find('ce:label', self.namespaces).text if subsection.find('ce:label', self.namespaces) is not None else None,
                        'title': subsection.find('ce:section-title', self.namespaces).text if subsection.find('ce:section-title', self.namespaces) is not None else None,
                        'paragraphs': [],
                        'subsections': []
                    }
                    
                    # Process paragraphs in subsections
                    for para in subsection.findall('ce:para', self.namespaces):
                        para_text = []
                        for elem in para.iter():
                            if elem.text and elem.text.strip():
                                para_text.append(elem.text.strip())
                            if elem.tag == f"{{{self.namespaces['ce']}}}cross-ref":
                                ref_text = ''.join(elem.itertext()).strip()
                                para_text.append(f"[{ref_text}]")
                            if elem.tail and elem.tail.strip():
                                para_text.append(elem.tail.strip())
                        
                        subsection_data['paragraphs'].append(' '.join(para_text))
                    
                    section_data['subsections'].append(subsection_data)
                
                sections.append(section_data)
            
            return pd.DataFrame(sections)
        else:
            subsection_data = {'paragraphs':[]}
            for section in root.findall('.//ce:sections', self.namespaces):
                for para in section.findall('ce:para', self.namespaces):
                                    para_text = []
                                    for elem in para.iter():
                                        if elem.text and elem.text.strip():
                                            para_text.append(elem.text.strip())
                                        if elem.tag == f"{{{self.namespaces['ce']}}}cross-ref":
                                            ref_text = ''.join(elem.itertext()).strip()
                                            para_text.append(f"[{ref_text}]")
                                        if elem.tail and elem.tail.strip():
                                            para_text.append(elem.tail.strip())
                                    
                                    subsection_data['paragraphs'].append(' '.join(para_text))
                
            return pd.DataFrame(subsection_data)
    
    def SerialItem_parse_references_headtail(self,xml_path):

        tree = ET.parse(xml_path)
        root = tree.getroot()
        bib_refs = root.findall('.//ce:bib-reference', namespaces=self.namespaces)

        records = []
        for bib in bib_refs:
            label = bib.findtext('ce:label', default='', namespaces=self.namespaces)
            sbref = bib.find('.//sb:reference', namespaces=self.namespaces)
            ce_other = bib.find('.//ce:other-ref', namespaces=self.namespaces)
            ce_source = bib.find('ce:source-text', namespaces=self.namespaces)
            if sbref is not None:
                title = sbref.find('.//sb:maintitle', namespaces=self.namespaces)
                year = sbref.find('.//sb:date', namespaces=self.namespaces)
                volume = sbref.find('.//sb:volume-nr', namespaces=self.namespaces)
                first_page = sbref.find('.//sb:first-page', namespaces=self.namespaces)
                last_page = sbref.find('.//sb:last-page', namespaces=self.namespaces)
                all_authors = sbref.findall('.//ce:surname', namespaces=self.namespaces)
                authors_str = [a.text for a in all_authors if a is not None]
                records.append({
                    'label': label,
                    'authors': authors_str,
                    'title': title.text if title is not None else '',
                    'year': year.text if year is not None else '',
                    'volume': volume.text if volume is not None else '',
                    'firstpage': first_page.text if first_page is not None else '',
                    'lastpage': last_page.text if last_page is not None else '',
                    'source_text': ce_source.text if ce_source is not None else ''
                })
            elif ce_other is not None:
                textref = ce_other.findtext('ce:textref', default='', namespaces=self.namespaces)
                records.append({
                    'label': label,
                    'authors': [],
                    'title': '',
                    'year': '',
                    'volume': '',
                    'firstpage': '',
                    'lastpage':'',
                    'source_text': textref or (ce_source.text if ce_source is not None else '')
                })
            else:
                records.append({
                    'label': label,
                    'authors': [],
                    'title': '',
                    'year': '',
                    'volume': '',
                    'firstpage': '',
                    'lastpage':'',
                    'source_text': ce_source.text if ce_source is not None else ''
                })

        df = pd.DataFrame(records)
        df.columns = ['label','authors','journal','year','volume','firstpage','lastpage','title']
        df = df[['label', 'authors', 'title', 'journal', 'year', 'firstpage','lastpage']]
        return df
    
    def SerialItem_parse_references(self,xmlfilepath):
        tree = etree.parse(xmlfilepath)
        root = tree.getroot()
        """Parse references/bibliography"""
        references = []
        bibliography = root.find('.//ce:bibliography', self.namespaces)
        
        if bibliography is not None:
            for ref in bibliography.findall('.//ce:bib-reference', self.namespaces):
                ref_data = {
                    'label': ref.find('ce:label', self.namespaces).text if ref.find('ce:label', self.namespaces) is not None else None,
                    'authors': [],
                    'title': None,
                    'journal': None,
                    'year': None,
                    'firstpage': None,
                    'lastpage': None
                }
                
                # Parse reference details
                sb_ref = ref.find('sb:reference',self.namespaces)
                if sb_ref is not None:
                    # Authors
                    for author in sb_ref.findall('.//sb:author', self.namespaces):
                        author_name = f"{author.find('ce:given-name', self.namespaces).text if author.find('ce:given-name', self.namespaces) is not None else ''} {author.find('ce:surname', self.namespaces).text if author.find('ce:surname', self.namespaces) is not None else ''}"
                        ref_data['authors'].append(author_name.strip())
                    
                    # Title
                    title = sb_ref.find('.//sb:maintitle', self.namespaces)
                    if title is not None:
                        ref_data['title'] = title.text
                    
                    # Journal and publication info
                    host = sb_ref.find('.//sb:host', self.namespaces)
                    if host is not None:
                        ref_data['journal'] = host.find('.//sb:maintitle', self.namespaces).text if host.find('.//sb:maintitle', self.namespaces) is not None else None
                        ref_data['year'] = host.find('.//sb:date', self.namespaces).text if host.find('.//sb:date', self.namespaces) is not None else None
                        pages = host.find('.//sb:pages', self.namespaces)
                        if pages is not None:
                            ref_data['firstpage'] = f"{pages.find('sb:first-page', self.namespaces).text if pages.find('sb:first-page', self.namespaces) is not None else ''}"
                            ref_data['lastpage'] = f"{pages.find('sb:last-page', self.namespaces).text if pages.find('sb:last-page', self.namespaces) is not None else ''}"
                
                references.append(ref_data)
        
        return pd.DataFrame(references)

    def parse_source_info (self, xmlfilepath):
        try:
            JournalTitle = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['journal_title']
        except:
            JournalTitle = ""
        try:
            Issn = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['issn']
        except:
            Issn = ""
        try:
            Volumn = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['volume']
        except:
            Volumn = ""
        try:
            Firstpage = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['first_page']
        except:
            Firstpage = ""
        try:
            Lastpage = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['last_page']
        except:
            Lastpage = ""
        try:
            JournalID = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['journal_id']
        except:
            JournalID = ""
        return pd.DataFrame([[JournalTitle,JournalID,Issn,Volumn,Firstpage,Lastpage]], columns=['JournalTitle','JournalID','Issn','Volumn','Firstpage','Lastpage'])

    def parse_article_coreinfo(self, xmlfilepath):
        try:
            PublicationDate = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['publication_date']
        except:
            PublicationDate = ""

        try:
            Doi = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['doi']
        except:
            Doi = ""

        try:
            Pii = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['pii']
        except:
            Pii = ""

        try:
            Eid = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['eid']
        except:
            Eid = ""

        try:
            DocumentType = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['documentType']
        except:
            DocumentType = ""

        try:
            DocumentSubType = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['documentSubType']
        except:
            DocumentSubType = ""

        try:
            OpenAccess = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['is_open_access']
        except:
            OpenAccess = ""

        try:
            License = self.Meta_parse_article_metadata(xmlfilepath).to_dict(orient='records')[0]['license']
        except:
            License = ""

        try:
            FirstAuthorSurname = self.Meta_parse_Normalize_FIRSTAuthors(xmlfilepath).to_dict(orient='records')[0]['surname']
        except:
            FirstAuthorSurname = ""

        try:
            FirstAuthorInitial = self.Meta_parse_Normalize_FIRSTAuthors(xmlfilepath).to_dict(orient='records')[0]['initials']
        except:
            FirstAuthorInitial = ""

        try:
            ArticleID = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['article_id']
        except:
            ArticleID = ""

        try:
            copyright = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['copyright']
        except:
            copyright = ""

        try:
            Title = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['title']
        except:
            Title = ""

        try:
            keywords = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['keywords']
        except:
            keywords = ""

        try:
            graphical_abstract = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['graphical_abstract']
        except:
            graphical_abstract = ""

        try:
            author_highlights = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['author_highlights']
        except:
            author_highlights = ""

        try:
            author_abstract = self.SerialItem_parse_Coredata(xmlfilepath).to_dict(orient='records')[0]['author_abstract']
        except:
            author_abstract = ""
        return pd.DataFrame([[
                                
                                PublicationDate, Doi, Pii, Eid, DocumentType, DocumentSubType,
                                OpenAccess, License, FirstAuthorSurname, FirstAuthorInitial,
                                ArticleID, copyright, Title, keywords, graphical_abstract,
                                author_highlights, author_abstract
                            ]],
                            columns=[
                                
                                'PublicationDate', 'Doi', 'Pii', 'Eid', 'DocumentType', 'DocumentSubType',
                                'OpenAccess', 'License', 'FirstAuthorSurname', 'FirstAuthorInitial',
                                'ArticleID', 'copyright', 'Title', 'keywords', 'graphical_abstract',
                                'author_highlights', 'author_abstract'
                            ]
                        )
    
    def parse_authors_info (self, xmlfilepath):
        return self.SerialItem_parse_authors(xmlfilepath)

    def parse_figures_info(self, xmlfilepath):
        return self.SerialItem_parse_figures(xmlfilepath)

    def parse_tables_info(self, xmlfilepath):
        return self.SerialItem_parse_tables(xmlfilepath)

    def parse_references_info(self, xmlfilepath):
        if self.get_xmlType(xmlfilepath) == 'HEAD-AND-TAIL':
            return self.SerialItem_parse_references_headtail(xmlfilepath)
        else:
            return self.SerialItem_parse_references(xmlfilepath)

    def parse_allAttachment_info(self, xmlfilepath):
        return self.Meta_parse_attachments(xmlfilepath)

    def parse_webfulltextPDF (self, xmlfilepath):
        return self.Meta_parse_webpdf(xmlfilepath)

    def parse_webfulltextIMG (self, xmlfilepath):
        return self.Meta_parse_webpdfimg(xmlfilepath)

    def parse_fundings_info(self, xmlfilepath):
        return self.Meta_parse_funding(xmlfilepath) 

    def parse_fulltext_info(self, xmlfilepath):
        if self.get_xmlType(xmlfilepath) == 'FULL-TEXT':
            return self.SerialItem_parse_sections(xmlfilepath)
        else:
            return self.SerialItem_parse_rawtext(xmlfilepath)
    