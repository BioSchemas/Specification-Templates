#!/usr/bin/env python3

import spec2model.markdown_parser as md_parser
bsc_md_parser = md_parser.FrontMatterParser()
bsc_md_parser.parse_front_matter()
