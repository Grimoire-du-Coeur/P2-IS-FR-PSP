import statistics
import shutil
import struct
import os
import io

COLUMN_STORAGE_MASK       = 0xf0
COLUMN_STORAGE_PERROW     = 0x50
COLUMN_STORAGE_CONSTANT   = 0x30
COLUMN_STORAGE_ZERO       = 0x10
COLUMN_TYPE_MASK          = 0x0f
COLUMN_TYPE_DATA          = 0x0b
COLUMN_TYPE_STRING        = 0x0a
COLUMN_TYPE_FLOAT         = 0x08
COLUMN_TYPE_8BYTE         = 0x06
COLUMN_TYPE_4BYTE2        = 0x05
COLUMN_TYPE_4BYTE         = 0x04
COLUMN_TYPE_2BYTE2        = 0x03
COLUMN_TYPE_2BYTE         = 0x02
COLUMN_TYPE_1BYTE2        = 0x01
COLUMN_TYPE_1BYTE         = 0x00

COLUMN_TYPE_MAP = {
    COLUMN_TYPE_DATA    : '>LL',
    COLUMN_TYPE_STRING  : '>L',
    COLUMN_TYPE_FLOAT   : '>f',
    COLUMN_TYPE_8BYTE   : '>Q',
    COLUMN_TYPE_4BYTE2  : '>l',
    COLUMN_TYPE_4BYTE   : '>L',
    COLUMN_TYPE_2BYTE2  : '>h',
    COLUMN_TYPE_2BYTE   : '>H',
    COLUMN_TYPE_1BYTE2  : '>b',
    COLUMN_TYPE_1BYTE   : '>B',
}

def chiper(data):
    c, m = (0x5f, 0x15)
    v = bytearray(data)
    for i in range(len(v)):
        v[i] = v[i] ^ c & 0xff
        c = c * m & 0xff
    return bytes(v)

class UTFReader:
    def __init__(self, data):
        if data.startswith(b'\x1F\x9E\xF3\xF5'):
            self.data = chiper(data)
            self.encrypted = True
        else:
            self.data = data
            self.encrypted = False
            
        f = io.BytesIO(self.data)
        self.marker, self.table_size = struct.unpack('>4sL', f.read(8))
        assert self.marker == b'@UTF'
        
        self.table_content = f.read(self.table_size)
        f = io.BytesIO(self.table_content)
        
        self.rows_offset, self.string_table_offset, self.data_offset, \
        self.table_name_string, self.column_length, self.row_width, \
        self.row_length = struct.unpack('>LLLLHHL', f.read(0x18))
        
        self.name = self.getstring(f, self.table_name_string)
        
        self.columns = []
        for i in range(self.column_length):
            typeid, nameoffset = struct.unpack('>BL', f.read(0x05))
            name = self.getstring(f, nameoffset)
            storagetype = typeid & COLUMN_STORAGE_MASK
            fieldtype = typeid & COLUMN_TYPE_MASK
            
            constant_data = None
            if storagetype == COLUMN_STORAGE_CONSTANT:
                pattern = COLUMN_TYPE_MAP[fieldtype]
                constant_data = struct.unpack(pattern, f.read(struct.calcsize(pattern)))
                if fieldtype == COLUMN_TYPE_STRING:
                    constant_data = (self.getstring(f, constant_data[0]),)
            
            self.columns.append({
                'name': name,
                'typeid': typeid,
                'storagetype': storagetype,
                'fieldtype': fieldtype,
                'constant_data': constant_data
            })
            
        f.seek(self.rows_offset, 0)
        self.rows = []
        for r in range(self.row_length):
            start_offset = f.tell()
            row = []
            for col in self.columns:
                if col['storagetype'] == COLUMN_STORAGE_CONSTANT:
                    row.append(col['constant_data'][0])
                elif col['storagetype'] == COLUMN_STORAGE_ZERO:
                    row.append(0)
                elif col['storagetype'] == COLUMN_STORAGE_PERROW:
                    pattern = COLUMN_TYPE_MAP[col['fieldtype']]
                    val = struct.unpack(pattern, f.read(struct.calcsize(pattern)))
                    if col['fieldtype'] == COLUMN_TYPE_STRING:
                        val = (self.getstring(f, val[0]),)
                    row.append(val[0] if len(val) == 1 else val)
            assert f.tell() - start_offset == self.row_width
            self.rows.append(row)
            
    def getstring(self, f, offset):
        pos = f.tell()
        f.seek(self.string_table_offset + offset, 0)
        s = b""
        while True:
            c = f.read(1)
            if c == b'\x00' or not c:
                break
            s += c
        f.seek(pos, 0)
        return s.decode('utf-8', errors='ignore')

class UTFWriter:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []
        self.rows = []
        self.strings = [table_name, "<NULL>"]
        
    def copy_schema_from(self, reader):
        for col in reader.columns:
            self.add_column(col['name'], col['typeid'], col['constant_data'])
            
    def add_column(self, name, typeid, constant_data=None):
        if name not in self.strings:
            self.strings.append(name)
        if constant_data and (typeid & COLUMN_TYPE_MASK) == COLUMN_TYPE_STRING:
            if constant_data[0] not in self.strings:
                self.strings.append(constant_data[0])
        self.columns.append({
            'name': name,
            'typeid': typeid,
            'constant_data': constant_data
        })
        
    def add_row(self, row_data):
        self.rows.append(row_data)
        for i, col in enumerate(self.columns):
            if (col['typeid'] & COLUMN_STORAGE_MASK) == COLUMN_STORAGE_PERROW and (col['typeid'] & COLUMN_TYPE_MASK) == COLUMN_TYPE_STRING:
                val = row_data[i]
                if isinstance(val, str) and val not in self.strings:
                    self.strings.append(val)
                    
    def build(self):
        for col in self.columns:
            col['storagetype'] = col['typeid'] & COLUMN_STORAGE_MASK
            col['fieldtype'] = col['typeid'] & COLUMN_TYPE_MASK
            
        for row in self.rows:
            for i, col in enumerate(self.columns):
                if col['storagetype'] == COLUMN_STORAGE_PERROW and col['fieldtype'] == COLUMN_TYPE_STRING:
                    val = row[i]
                    if isinstance(val, str) and val not in self.strings:
                        self.strings.append(val)
                        
        string_offsets = {}
        string_data = b""
        for s in self.strings:
            string_offsets[s] = len(string_data)
            string_data += s.encode('utf-8') + b'\x00'
            
        schema_data = b""
        row_width = 0
        for col in self.columns:
            name_off = string_offsets[col['name']]
            schema_data += struct.pack('>BL', col['typeid'], name_off)
            stype = col['storagetype']
            ftype = col['fieldtype']
            
            if stype == COLUMN_STORAGE_CONSTANT:
                pattern = COLUMN_TYPE_MAP[ftype]
                val = col['constant_data']
                if ftype == COLUMN_TYPE_STRING:
                    val = (string_offsets[val[0]],)
                schema_data += struct.pack(pattern, *val)
            elif stype == COLUMN_STORAGE_PERROW:
                pattern = COLUMN_TYPE_MAP[ftype]
                row_width += struct.calcsize(pattern)
                
        rows_data = b""
        for row in self.rows:
            for i, col in enumerate(self.columns):
                stype = col['storagetype']
                ftype = col['fieldtype']
                if stype == COLUMN_STORAGE_PERROW:
                    val = row[i]
                    pattern = COLUMN_TYPE_MAP[ftype]
                    if ftype == COLUMN_TYPE_STRING:
                        val = (string_offsets[val], )
                    elif not isinstance(val, tuple):
                        val = (val, )
                    rows_data += struct.pack(pattern, *val)
                    
        schema_offset = 0x18
        rows_offset = schema_offset + len(schema_data)
        
        string_table_offset = rows_offset + len(rows_data)
        data_offset = string_table_offset + len(string_data)
        table_size = data_offset + 8
        
        out = b"@UTF"
        out += struct.pack('>L', data_offset) # table size
        out += struct.pack('>L', rows_offset)
        out += struct.pack('>L', string_table_offset)
        out += struct.pack('>L', data_offset)
        out += struct.pack('>L', string_offsets[self.table_name])
        out += struct.pack('>H', len(self.columns))
        out += struct.pack('>H', row_width)
        out += struct.pack('>L', len(self.rows))
        
        out += schema_data
        out += rows_data
        out += string_data
        return out


def extract_cpk(cpk_path, out_dir):
    with open(cpk_path, 'rb') as f:
        magic = f.read(4)
        if magic != b'CPK ':
            raise ValueError("Not a CPK file")
            
        f.seek(0)
        chunk = f.read(2048)
        header_utf = UTFReader(chunk[0x10:])
        
        cols = {c['name']: i for i, c in enumerate(header_utf.columns)}
        toc_offset = header_utf.rows[0][cols['TocOffset']]
        toc_size = header_utf.rows[0][cols['TocSize']]
        content_offset = header_utf.rows[0][cols['ContentOffset']]
        baseline = min(toc_offset, content_offset)
        content_offset = header_utf.rows[0][cols['ContentOffset']]
        
        baseline = min(toc_offset, content_offset)
        
        f.seek(toc_offset)
        toc_data = f.read(toc_size)
        toc_utf = UTFReader(toc_data[0x10:])
        
        cols_toc = {c['name']: i for i, c in enumerate(toc_utf.columns)}
        
        for row in toc_utf.rows:
            dirname = row[cols_toc['DirName']]
            filename = row[cols_toc['FileName']]
            if not filename:
                continue
            size = row[cols_toc['ExtractSize']] # Or FileSize. Some are CRILAYLA compressed. 
            offset = row[cols_toc['FileOffset']]
            
            if not filename:
                continue
                
            file_path = os.path.join(out_dir, dirname, filename) if dirname else os.path.join(out_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            f.seek(baseline + offset)
            file_data = f.read(size) # Read ExtractSize (Wait! If it's CRILAYLA compressed, FileSize is the compressed size! ExtractSize is uncompressed size. We should read FileSize! Let's read FileSize first)
            
            # Correction: read FileSize to get exact bytes on disk
            real_size = row[cols_toc['FileSize']]
            f.seek(baseline + offset)
            file_data = f.read(real_size)
            
            # Let's not decompress CRILAYLA for now, just extract raw files
            # If the user edits GIMs, they just overwrite the raw files.
            with open(file_path, 'wb') as out_f:
                out_f.write(file_data)
                
    return True

def align(offset, alignment=2048):
    remainder = offset % alignment
    if remainder != 0:
        return offset + (alignment - remainder)
    return offset
    
def build_cpk(in_dir, out_cpk_path, original_cpk_path):
    """
    Builds a CPK by doing an 'in-place' patch of the original CPK.
    This preserves the ITOC perfectly, preserves all file paddings,
    and simply appends modified files to the end of the CPK while updating
    the original TOC FileOffset, FileSize, and ExtractSize values.
    """
    print("Copie du CPK original...")
    shutil.copyfile(original_cpk_path, out_cpk_path)
    
    with open(out_cpk_path, 'r+b') as f:
        f.seek(0)
        magic = f.read(4)
        if magic != b'CPK ':
            raise ValueError("Not a CPK")
            
        f.seek(0x10)
        chunk = f.read(2048)
        header_utf = UTFReader(chunk)
        cols = {c['name']: i for i, c in enumerate(header_utf.columns)}
        toc_offset = header_utf.rows[0][cols['TocOffset']]
        toc_size = header_utf.rows[0][cols['TocSize']]
        content_offset = header_utf.rows[0][cols['ContentOffset']]
        baseline = min(toc_offset, content_offset)
        
        f.seek(toc_offset)
        toc_data = f.read(toc_size)
        toc_utf = UTFReader(toc_data[0x10:])
        toc_data_offset = toc_utf.data_offset
        row_width = toc_utf.row_width
        
        cols_toc = {c['name']: i for i, c in enumerate(toc_utf.columns)}
        
        col_offsets = {}
        curr = 0
        for col in toc_utf.columns:
            if col['storagetype'] == 0x50: # COLUMN_STORAGE_PERROW
                col_offsets[col['name']] = curr
                pattern = {
                    0: '>B', 1: '>b', 2: '>H', 3: '>h', 4: '>I', 5: '>i',
                    6: '>Q', 7: '>q', 8: '>f', 10: '>I', 11: '>I'
                }.get(col['fieldtype'], '>I')
                curr += struct.calcsize(pattern)
                
        fs_off = col_offsets['FileSize']
        es_off = col_offsets['ExtractSize']
        fo_off = col_offsets.get('FileOffset')
        if fo_off is None:
            raise ValueError("FileOffset not found in TOC!")
            
        fo_col = next((c for c in toc_utf.columns if c['name'] == 'FileOffset'), None)
        if fo_col and fo_col['fieldtype'] == 6:
            fo_pattern = '>Q'
        else:
            fo_pattern = '>I'
        
        file_map = {}
        for root, dirs, files in os.walk(in_dir):
            for fname in files:
                file_map[fname] = os.path.join(root, fname)
                
        f.seek(0, 2)
        end_offset = f.tell()
        current_offset = align(end_offset, 2048)
        
        print("Analyse des fichiers pour patching IN-PLACE...")
        
                # Compute median mtime to detect modified files reliably
        mtimes = []
        for root_dir, _, files in os.walk(in_dir):
            for fname in files:
                if fname.startswith('_') or fname.endswith('.iso'): continue
                mtimes.append(os.path.getmtime(os.path.join(root_dir, fname)))
        
        median_time = statistics.median(mtimes) if mtimes else 0
        print(f'Median extraction time: {median_time}')
        
        for row_idx, row in enumerate(toc_utf.rows):
            dirname = row[cols_toc.get('DirName', -1)] if 'DirName' in cols_toc else ""
            filename = row[cols_toc['FileName']]
            if not filename:
                continue
            
            file_path = os.path.join(in_dir, dirname, filename) if dirname else os.path.join(in_dir, filename)
            if not os.path.exists(file_path) and filename in file_map:
                file_path = file_map[filename]
                
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f_in:
                    raw_data = f_in.read()
                    
                orig_size = row[cols_toc['FileSize']]
                orig_extract = row[cols_toc['ExtractSize']]
                
                file_mtime = os.path.getmtime(file_path)
                
                # If the file hasn't been modified since extraction (plus a 5 min margin), skip it!
                if file_mtime <= median_time + 300:
                    continue
                
                print(f'Modification detectee pour {filename} (mtime: {file_mtime} > median: {median_time})')
                
                    
                print(f"Modification de {filename}... (Nouveau offset: 0x{current_offset:X})")
                
                compressed = compress_crilayla(raw_data)
                
                f.seek(current_offset)
                f.write(compressed)
                new_size = len(compressed)
                new_extract = len(raw_data)
                
                patch_offset = toc_offset + 0x10 + 8 + toc_utf.rows_offset + row_idx * row_width
                
                f.seek(patch_offset + fs_off)
                f.write(struct.pack(">I", new_size))
                
                f.seek(patch_offset + es_off)
                f.write(struct.pack(">I", new_extract))
                
                f.seek(patch_offset + fo_off)
                f.write(struct.pack(fo_pattern, current_offset - baseline))
                
                current_offset += new_size
                current_offset = align(current_offset, 2048)
                
    return True

def extract_cpk(cpk_path, out_dir):
    """
    Extracts all files from a CPK archive.
    If files are CRILAYLA compressed, they will be decompressed automatically.
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(cpk_path, 'rb') as f:
        magic = f.read(4)
        if magic != b'CPK ':
            print("Erreur: Le fichier n'est pas une archive CPK valide.")
            return False
            
        f.seek(0)
        chunk = f.read(2048)
        header_utf = UTFReader(chunk[0x10:])
        
        cols = {c['name']: i for i, c in enumerate(header_utf.columns)}
        toc_offset = header_utf.rows[0][cols['TocOffset']]
        toc_size = header_utf.rows[0][cols['TocSize']]
        content_offset = header_utf.rows[0][cols['ContentOffset']]
        baseline = min(toc_offset, content_offset)
        content_offset = header_utf.rows[0][cols['ContentOffset']]
        
        # Read TOC
        f.seek(toc_offset)
        toc_data = f.read(toc_size)
        toc_utf = UTFReader(toc_data[0x10:])
        
        cols_toc = {c['name']: i for i, c in enumerate(toc_utf.columns)}
        
        file_count = len(toc_utf.rows)
        print(f"Extraction de {file_count} fichiers vers {out_dir}...")
        
        for idx, row in enumerate(toc_utf.rows):
            dirname = row[cols_toc['DirName']]
            filename = row[cols_toc['FileName']]
            if not filename:
                continue
            file_size = row[cols_toc['FileSize']]
            file_offset = row[cols_toc['FileOffset']]
            
            dir_path = os.path.join(out_dir, dirname) if dirname else out_dir
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                
            out_file = os.path.join(dir_path, filename)
            
            # Since ContentOffset in CPK header is the absolute start of files
            # But wait, FileOffset is sometimes relative to ContentOffset, sometimes absolute.
            # Usually if ContentOffset > 0 and FileOffset < ContentOffset, it's relative.
            # To be safe, many tools just assume FileOffset + ContentOffset or FileOffset depending on TOC.
            # In our case:
            baseline = min(toc_offset, content_offset)
            abs_offset = baseline + file_offset
            
            f.seek(abs_offset)
            file_data = f.read(file_size)
            
            # Decompress if CRILAYLA
            if file_data.startswith(b"CRILAYLA"):
                file_data = decompress_crilayla(file_data)
                
            with open(out_file, 'wb') as out_f:
                out_f.write(file_data)
                
            if (idx + 1) % 100 == 0:
                print(f"  {idx + 1}/{file_count} fichiers extraits...")
                
    print("Extraction terminee !")
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Outil CPK autonome (Pack/Unpack parfait avec CRILAYLA)")
    subparsers = parser.add_subparsers(dest="command", help="Commandes")

    extract_parser = subparsers.add_parser("extract", help="Extraire un fichier CPK")
    extract_parser.add_argument("input_cpk", help="Chemin vers le fichier .cpk d'entree")
    extract_parser.add_argument("out_dir", help="Dossier de sortie")

    rebuild_parser = subparsers.add_parser("rebuild", help="Reconstruire un fichier CPK")
    rebuild_parser.add_argument("input_dir", help="Dossier contenant les fichiers modifies (et/ou extraits)")
    rebuild_parser.add_argument("original_cpk", help="Chemin vers le fichier .cpk original (pour la base)")
    rebuild_parser.add_argument("out_cpk", help="Chemin vers le fichier .cpk de sortie")

    args = parser.parse_args()

    if args.command == "extract":
        extract_cpk(args.input_cpk, args.out_dir)
    elif args.command == "rebuild":
        build_cpk(args.input_dir, args.out_cpk, args.original_cpk)
        print(f"CPK reconstruit avec succes : {args.out_cpk}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
import sys
import os
import shutil
import struct
import statistics

class BitWriter:
    def __init__(self, size):
        self.buffer = bytearray(size)
        self.pos = size - 1
        self.flag = 0
        self.bits_left = 8

    def set_bits(self, value, bit_count):
        while bit_count > 0:
            if self.bits_left == 0:
                self.buffer[self.pos] = self.flag
                self.pos -= 1
                self.flag = 0
                self.bits_left = 8

            write = min(self.bits_left, bit_count)
            shift = bit_count - write
            bits = (value >> shift) & ((1 << write) - 1)
            self.flag |= (bits << (self.bits_left - write))

            self.bits_left -= write
            bit_count -= write

    def flush(self):
        if self.bits_left != 8:
            self.buffer[self.pos] = self.flag
            self.pos -= 1
        return self.buffer[self.pos + 1:]

class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = len(data) - 1
        self.flag = 0
        self.bits_left = 0
        
    def get_bits(self, bit_count):
        value = 0
        while bit_count > 0:
            if self.bits_left == 0:
                self.flag = self.data[self.pos]
                self.pos -= 1
                self.bits_left = 8
                
            read = min(self.bits_left, bit_count)
            value <<= read
            value |= (self.flag >> (self.bits_left - read)) & ((1 << read) - 1)
            self.bits_left -= read
            bit_count -= read
        return value

def compress_crilayla(data: bytes) -> bytes:
    # 256 bytes header
    if len(data) == 0:
        return b""
        
    header_size = min(len(data), 0x100)
    uncomp_header = data[:header_size]
    
    source = data[header_size:]
    if not source:
        comp_size = 0
        out = b"CRILAYLA"
        out += struct.pack("<I", len(data) - header_size)
        out += struct.pack("<I", comp_size)
        out += uncomp_header
        return out
        
    source = source[::-1]
    
    window_size = 8192
    min_len = 3
    max_len = 0
    
    length = len(source)
    pos = 0
    lookup = {}
    matches = []
    
    while pos < length:
        best_len = 0
        best_dist = 0
        
        if pos + min_len <= length:
            seq = source[pos:pos+min_len]
            if seq in lookup:
                for match_pos in reversed(lookup[seq]):
                    dist = pos - match_pos
                    if dist > window_size:
                        continue # Removed the break because the dictionary iteration is NOT guaranteed to be sorted by distance depending on how we stored it! Wait, we append in order, so reversed means newest first. But we still need to handle it properly. Let's just continue.
                    if dist < 3:
                        continue
                        
                    mlen = min_len
                    while mlen < max_len and pos + mlen < length and source[pos + mlen] == source[match_pos + mlen]:
                        mlen += 1
                        
                    if mlen > best_len:
                        best_len = mlen
                        best_dist = dist
                        if best_len == max_len:
                            break
                            
        if best_len >= min_len:
            matches.append((best_dist, best_len))
            for i in range(best_len):
                if pos + i + min_len <= length:
                    s = source[pos+i:pos+i+min_len]
                    if s not in lookup: lookup[s] = []
                    lookup[s].append(pos + i)
                    if len(lookup[s]) > 20:
                        lookup[s].pop(0)
            pos += best_len
        else:
            matches.append((source[pos],))
            if pos + min_len <= length:
                s = source[pos:pos+min_len]
                if s not in lookup: lookup[s] = []
                lookup[s].append(pos)
                if len(lookup[s]) > 20:
                    lookup[s].pop(0)
            pos += 1
            
    bw = BitWriter(int(len(source) * 1.5 + 1024))
    vle_levels = [2, 3, 5, 8]
    vle_flags = [3, 7, 0x1F, 0xFF]
    
    for m in matches:
        if len(m) == 1:
            bw.set_bits(0, 1)
            bw.set_bits(m[0], 8)
        else:
            bw.set_bits(1, 1)
            dist, l = m
            bw.set_bits(dist - 3, 13)
            
            vle = 0
            l_val = l - 3
            while l_val >= vle_flags[vle]:
                bw.set_bits(vle_flags[vle], vle_levels[vle])
                l_val -= vle_flags[vle]
                if vle != 3:
                    vle += 1
            bw.set_bits(l_val, vle_levels[vle])
            
    comp_payload = bw.flush()
    comp_size = len(comp_payload)
    
    out = b"CRILAYLA"
    out += struct.pack("<I", len(data) - header_size)
    out += struct.pack("<I", comp_size)
    out += comp_payload
    out += uncomp_header
    return out

def decompress_crilayla(data: bytes) -> bytes:
    if not data.startswith(b"CRILAYLA"):
        return data
        
    uncomp_size = struct.unpack("<I", data[8:12])[0]
    comp_size = struct.unpack("<I", data[12:16])[0]
    
    comp_payload = data[16:16+comp_size]
    uncomp_header = data[16+comp_size:16+comp_size+256]
    
    br = BitReader(comp_payload)
    dest = bytearray(uncomp_size)
    dest_pos = uncomp_size - 1
    
    vle_levels = [2, 3, 5, 8]
    vle_flags = [3, 7, 0x1F, 0xFF]
    
    while dest_pos >= 0:
        if br.get_bits(1) == 1:
            dist = br.get_bits(13) + 3
            l = 3
            vle = 0
            while True:
                val = br.get_bits(vle_levels[vle])
                l += val
                if val != vle_flags[vle]:
                    break
                if vle != 3:
                    vle += 1
                    
            for i in range(l):
                dest[dest_pos] = dest[dest_pos + dist]
                dest_pos -= 1
        else:
            dest[dest_pos] = br.get_bits(8)
            dest_pos -= 1
            
    return uncomp_header + dest
