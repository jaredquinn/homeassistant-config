
entity_id = data.get('entity_id')
state = None
command = data.get('command')
selected = data.get('selected')
previous = data.get('previous')

logger.info('Entity ID = %s, State = %s, Command %s = %s (old: %s)' % (entity_id, state, command, selected, previous))

commands = {
  'soniq': {
      'power': 'JgBIAAABKZMSEhI3EhIRExI2EjcROBETETgRExA4EzYROBEUEDcSNxISEzYRNxE4FBASEhMSEhIROBQQERMSEhI3EjYTNhI2EgANBQ'
  },
  'pioneer': {
      'satcbl': 'JgCQAAABGIkTMxMQEzMTEBMREjMTERIzExESMxMREjMTMxMQEzMTEBMQExETEBMQEzMTEBMQExETMhMzEzMTMhQQEzITMxMzEwADbAABGYgUMhQPFDIUDxQPFDIUDxQyFA8UMhQPFDIUMhQPFDIUDxQPExETEBMQEzMTEBMQExETMhMzEzMTMhQQEzIUMhMzEwANBQAAAAAAAAAA',
      'dvd': 'JgAgAQABGYgUMhMREzITERMQEzITERMyEhITMhISEzISNBESEzMREhI0ERISNBESEhIREhESETUREhE1ERIRNRE0EjQSNBESEQADbgABFosSNBESEjQREhISETQSEhE0EhIRNBISETQSNBESEjQREhE1ERIRNRESERMREhESETUREhE1ERIRNRE0EjQRNRESEQADbQABF4sRNRESETUREhESETUREhE1ERIRNRESETURNBISETQSEhE0EhIRNBISERIREhISETQSEhE0EhIRNBI0ETURNBISEQADbQABFosSNBESEjQREhISETQRExE0ERMRNBETETQRNRESETUREhE1ERIRNRESERISEhESETQSEhE0EhIRNBI0ETURNRESEQANBQAAAAAAAAAA',
      'bd': 'JgAgAQABGYgTMxMREjMTERIREzITERMyEhITMhISEzAUNBESEjQREhISERIRNBI0EjQREhI0ERISNBE1ERIREhETETQRExE0EQADbgABFosSNBESEjQREhISETQSEhE0EhIRNBISETQRNRESETUREhESEhIREhESERMREhE0EjQRNRE0EjQSNBE1ETQSEhESEQADbQABFowRNBISETQSEhESETQSEhE0EhIRNBISETQSNBISETQRExESERIRNRE0EjQREhI0ERISNBE1ERIREhISETQSEhE0EgADbQABFosSNBETETQRExESETQSEhE0EhIRNBISETQSNBESEjQREhISERIREhESEhIREhE1ETQSNBE1ETQSNBE1ETQSEhESEQANBQAAAAAAAAAA',
      'mute': 'JgDYAAABGIgUMhMPFDIUDhMPEzMTDxMzEw8UMhMPFDEUMhMPFDITDxQPEzIUDhMQEzIUDxMPEw8UMhQPEzIUMRQPEzIUMhMyFQADOAABGIgUMhMPFDIUDhQPEzIUDhQyEw8UMhMPFDITMhQOFDITDxQPEzIUDxMPFDITDxMPEw8UMhQPEzIUMhMPFDEUMhMyFAADOQABF4oUMRMPFDITDxQPEzIUDxMyExATMhMPFDIUMRQPEzITDxQPEzIUDxMPFDITDxQPEw8UMRMPFDIUMhMPFDITMhMyFAANBQ'
  },
  'fetch': {
      '1': 'JgBQAAABKJEUERQREzYUERQRFDYTNhQRFBETNhQ2FBETEhMRFDYTEhMSEzYUERMSExEUERQRExITNhQRFDYTNhQ2EzYUNhQ2EwAFZQABKEkTAA0FAAAAAAAAAAA',
      '2': 'JgBQAAABKJEVEBQREzYUERQRFDUUNhQRFBETNhQ2ExITERQRFDYTEhM2FDYTEhMRFBEUERMSExEUERQREzYUNhQ2EzYUNhQ1FAAFZQABKEgVAA0FAAAAAAAAAAA',
      '3': 'JgBQAAABJ5MSExISEjgRFBEUETgSOBITEhISOBE5ERMSExEUETgSExITEhMSNxMSEhMRFBETEhMSOBI3ExIRORI3EjgSNxI4EgAFZgABJksRAA0FAAAAAAAAAAA',
      '4': 'JgBYAAABJ5MRExITETkSEhITEjgROBITEhMRORE4EhMSExETEjgRFBE4EhMSOBITEhISExITEhMRExM3ERQROBI4EjgROBI4EQAFZwABJksSAAxLAAEnShIADQU',
      '5': 'JgBQAAABJpQSEhITEjgRFBETEjgSNxMSEhMRORE4EhMRFBEUETgRFBITETgTNxITEhISExEUERQROBMSEhQRNxI4EjgROBI4EQAFZwABJ0oRAA0FAAAAAAAAAAA',
      '6': 'JgBQAAABJpMSExEUETgSExITETgSOBEUERQROBI4ERQRExITETkSExI3EjgROBITERQRFBEUERMSExEUEhMROBE5ETgSOBE4EgAFZwABJkoSAA0FAAAAAAAAAAA',
      '7': 'JgBQAAABJ5ISExMSETkSEhITEjgSNxMSERQSNxI4ERQSExEUEjcSExEUEhMSExA5EhMRExITExISNxM3EjgRExI4EjgROBI4EgAFZgABJ0oSAA0FAAAAAAAAAAA',
      '8': 'JgBQAAABJ5ISExEUETkRExITETkROBITERQROBI2FBMRFBETEjgRFBE4EhMRFBI3EhMRFBEUERMSExI4ETgSExI4ETgSOBI4EQAFZwABJkoSAA0FAAAAAAAAAAA',
      '9': 'JgBYAAABJ5ISExITETkSEhITETkROBITERQROBM3ERQSExETEzcRFBETEjgRFBE4EhMSExEUERQROBITETgTEhI4EjcSOBE5EQAFZwABJkoSAAxMAAEmShIADQU',
      '0': 'JgBQAAABJpQSExITETgSExEUETgSOBEUERMSOBE5EhISExITEjgRExI4ETkRExI4ERQRFBETEhMRFBETEjgRFBE4EjgRORE4EgAFZgABJ0oSAA0FAAAAAAAAAAA',
  }
}

word_map = {
        'a BC news': 'ABC News',
        'ten': 'TEN HD',
        '10': 'TEN HD',
        '11': 'Eleven',
        'eleven': 'Eleven',
        'one': 'One',
        'France 24': 'France24',
        '1': 'One',
        'shopping': 'TVSN',
        'spree': 'SpreeTV',
        'ABC': 'ABC HD',
        'news': 'ABC News',
        'ABC news': 'ABC News',
        'ABC News': 'ABC News',
        'ABC comedy': 'ABC comedy',
        'me': 'ABC Me',
        'SBS': 'SBS HD',
        'SBS Food': 'SBS Food Network',
        'viceland': 'SBS Viceland',
        'vice': 'SBS Viceland',
        'nitv': 'NITV',
        'seven': '7 HD',
        '72': '7two',
        'seven two': '7two',
        'seven mate': '7mate',
        '7mate': '7mate',
        'seven flicks': '7flix',
        'seven flix': '7flix',
        'racing': 'Racing',
        '9': '9 HD',
        'Nine': '9 HD',
        'nine': '9 HD',
        '9 gem': '9Gem',
        'gem': '9Gem',
        'GEM': '9Gem',
        '9 go': '9Go',
        'GO': '9Go',
        'life': '9Life',
        '9 life': '9Life',
        '9 live': '9Life',
        'extra': 'Extra',
        'TV hits': 'TV Hits',
        'mtv': 'MTV',
        'entertainment': 'E!',
        'style': 'Style',
        'BBC News': 'BBC World News',
        'BBC first': 'BBC First',
        'UKTV': 'BBC UKTV',
        'UK TV': 'BBC UKTV',
        'BBC UK TV': 'BBC UKTV',
        'universal': 'Universal',
        'comedy': 'Comedy Central',
        'ABC comedy': 'ABC Comedy',
        'Syfy': 'SyFy',
        'sci-fi': 'SyFy',
        'Sci-Fi': 'SyFy',
        'science fiction': 'SyFy',
        'thirtheenth': '13th Street',
        'funny': '111 Funny',
        'spike': 'Spike',
        'ESPN': 'ESPN',
        'ESPN2': 'ESPN 2',
        'espn2': 'ESPN 2',
        'sports': 'ESPN',
        'sports two': 'ESPN 2',
        'edge': 'Edge',
        'Nat Geo people': 'Nat Geo People',
        'national geographic': 'Nat Geo',
        'wild': 'Nat Geo Wild',
        'HGTV': 'HGTV',
        'hgtv': 'HGTV',
        'home and garden TV': 'HGTV',
        'home and garden': 'HGTV',
        'food network': 'Food Network',
        'travel': 'Travel Channel',
        'travel channel': 'Travel Channel',
        'music': 'MTV Music',
        'MTV music': 'MTV Music',
        'classic music': 'MTV Classic',
        'MTV classic': 'MTV Classic',
        'dance music': 'MTV Dance',
        'MTV dance': 'MTV Dance',
        'egg': 'EGG',
        'al jazeera': 'Al Jazerra'
}


channels = {
    'TEN HD': '013',
    'Eleven': '011',
    'One': '012',
    'TVSN': '014',
    'SpreeTV': '015',
    'ABC HD': '020',
    'ABC News': '024',
    'ABC Comedy': '022',
    'ABC Me': '023',
    'SBS HD': '030',
    'SBS Viceland': '032',
    'SBS Food Network': '033',
    'NITV': '034',
    '7 HD': '070',
    '7two': '072',
    '7mate': '073',
    '7flix': '076',
    'Racing': '078',
    '9 HD': '090',
    '9Gem': '092',
    '9Go': '093',
    '9Life': '094',
    'Extra': '095',
    'TV Hits': '101',
    'MTV': '102',
    'E!': '103',
    'Style': '104',
    'BBC First': '105',
    'BBC UKTV': '106',
    'Universal': '107',
    'Comedy Central': '108',
    'SyFy': '109',
    '13th Street': '110',
    '111 Funny': '111',
    'Spike': '112',
    'ESPN': '115',
    'ESPN 2': '116',
    'Edge': '119',
    'Nat Geo': '121',
    'Nat Geo Wild': '123',
    'BBC Knowledge': '124',
    'HGTV': '126',
    'Food Network': '127',
    'Nat Geo People': '130',
    'Travel Channel': '131',
    'Fashion TV': '138',
    'MTV Music': '139',
    'MTV Classic': '140',
    'MTV Dance': '141',
    'CMusic': '142',
    'EGG': '143',
    'Disney': '144',
    'Disney Jr': '145',
    'Nickelodeon': '146',
    'Nick Jr': '147',
    'Disney XD': '148',
    'Cartoon Network': '149',
    'Boomerang': '150',
    'CBeebies': '151',
    'ZooMoo': '152',
    'Baby TV': '153',
    'CNN': '179',
    'BBC World News': '180',
    'CNBC': '181',
    'Bloomberg': '182',
    'France24': '183',
    'euronews': '184',
    'NDTV 24x7': '185',
    'newsAsia': '186',
    'Al Jazeera': '187',
    'CGTN': '188',
    'Radio: Double J': '200',
    'Radio: ABC Jazz': '201',
}

def make_remote_sequence(device, key):
    c = []
    for i in key:
        c.append( device[i] )
    return c


if command == 'word':

    channel = word_map.get(selected, selected)
    if channel:
        hass.states.set(entity_id, channel, { }, force_update=True)
        #hass.services.call('input_select', 'select_option', { 'option': channel} )

if command == 'mute':

    packets = [ commands['pioneer']['mute'] ]

if command == 'source' or command == 'channel':

    if command == 'source':
        if selected == 'Fetch TV':
            packets = [ commands['pioneer']['satcbl'] ]

        if selected == 'Chromecast':
            packets = [ commands['pioneer']['dvd'] ]

        if selected == 'Roku':
            packets = [ commands['pioneer']['bd'] ]

    if command == 'channel':
        packets = make_remote_sequence(commands['fetch'], channels[selected])

    if len(packets) > 0:
        hass.services.call('broadlink', 'send_packet_10_10_98_31', { 'packet': packets } )

