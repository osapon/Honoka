#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Honoka の Bootstrap 4 サンプル HTML を Bootstrap 5 向けに変換するスクリプト。
"""

import re
import sys
from pathlib import Path


def replace_data_attrs(html: str) -> str:
    """Bootstrap 5 では data-* が data-bs-* に変更された属性を置換する。"""
    targets = ['toggle', 'target', 'dismiss', 'placement', 'content', 'container']
    for t in targets:
        # data-toggle= などを data-bs-toggle= に
        html = re.sub(rf'\bdata-{t}=', rf'data-bs-{t}=', html)
    return html


def replace_utility_classes(html: str) -> str:
    """BS4 のユーティリティクラスを BS5 に置き換える。"""
    # マージン・パディング方向
    html = re.sub(r'\bmr-', 'me-', html)
    html = re.sub(r'\bml-', 'ms-', html)
    html = re.sub(r'\bpr-', 'pe-', html)
    html = re.sub(r'\bpl-', 'ps-', html)

    # テキスト揃え
    html = re.sub(r'\btext-right\b', 'text-end', html)
    html = re.sub(r'\btext-left\b', 'text-start', html)
    html = re.sub(r'\btext-xl-left\b', 'text-xl-start', html)

    # その他
    html = re.sub(r'\bsr-only\b', 'visually-hidden', html)
    html = re.sub(r'\bform-inline\b', 'd-flex flex-nowrap align-items-center', html)
    html = re.sub(r'\bform-group\b', 'mb-3', html)
    html = re.sub(r'\bbtn-block\b', 'w-100 d-block', html)
    html = re.sub(r'\btext-muted\b', 'text-body-secondary', html)

    return html


def replace_badges(html: str) -> str:
    """badge クラスを BS5 形式に置き換える。"""
    colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
    # まず badge-* 色クラスを text-bg-* に置き換える
    # 対象: badge badge-primary / badge badge-pill badge-primary など
    for c in colors:
        html = re.sub(rf'\bbadge-{c}\b', f'text-bg-{c}', html)
    # 次に badge-pill を rounded-pill に置き換える
    html = re.sub(r'\bbadge-pill\b', 'rounded-pill', html)
    return html


def replace_custom_forms(html: str) -> str:
    """custom-* 系フォームを BS5 の form-check / form-select / form-range に置き換える。"""
    # ラジオ / チェックボックス / スイッチ
    html = re.sub(
        r'<div class="custom-control custom-radio">',
        '<div class="form-check">',
        html
    )
    html = re.sub(
        r'<div class="custom-control custom-checkbox">',
        '<div class="form-check">',
        html
    )
    html = re.sub(
        r'<div class="custom-control custom-switch">',
        '<div class="form-check form-switch">',
        html
    )
    html = re.sub(r'\bcustom-control-input\b', 'form-check-input', html)
    html = re.sub(r'\bcustom-control-label\b', 'form-check-label', html)
    html = re.sub(r'\bcustom-select\b', 'form-select', html)
    html = re.sub(r'\bcustom-range\b', 'form-range', html)
    html = re.sub(r'\bform-control-file\b', 'form-control', html)
    return html


def replace_input_group_addons(html: str) -> str:
    """input-group-prepend / input-group-append を BS5 形式に簡略化する。"""
    # <div class="input-group-prepend"><span class="input-group-text">X</span></div>
    # → <span class="input-group-text">X</span>
    html = re.sub(
        r'<div class="input-group-prepend">\s*<span class="input-group-text">([^<]*)</span>\s*</div>',
        r'<span class="input-group-text">\1</span>',
        html
    )
    html = re.sub(
        r'<div class="input-group-append">\s*<span class="input-group-text">([^<]*)</span>\s*</div>',
        r'<span class="input-group-text">\1</span>',
        html
    )
    return html


def replace_custom_file(html: str) -> str:
    """custom-file を BS5 のネイティブ file input + input-group-text に置き換える。"""
    def repl(m):
        input_id = m.group(1)
        label_text = m.group(2)
        upload_text = m.group(3)
        return (
            f'<input type="file" class="form-control" id="{input_id}" aria-label="{label_text}">\n'
            f'                <span class="input-group-text">{upload_text}</span>'
        )

    html = re.sub(
        r'<div class="custom-file">\s*<input type="file" class="custom-file-input" id="([^"]+)">\s*<label class="custom-file-label" for="[^"]+">([^<]*)</label>\s*</div>\s*<div class="input-group-append">\s*<span class="input-group-text" id="">([^<]*)</span>\s*</div>',
        repl,
        html
    )
    return html


def replace_close_buttons(html: str) -> str:
    """BS4 の close ボタンを BS5 の btn-close に置き換える。"""
    # <button type="button" class="close" data-bs-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
    # → <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    html = re.sub(
        r'<button type="button" class="close"([^>]*)>\s*<span aria-hidden="true">&times;</span>\s*</button>',
        r'<button type="button" class="btn-close"\1></button>',
        html
    )
    # <span> で囲まれていない &times; も対応
    html = re.sub(
        r'<button type="button" class="close"([^>]*)>\s*&times;\s*</button>',
        r'<button type="button" class="btn-close"\1 aria-label="Close"></button>',
        html
    )
    # toast-header 内の ml-2 mb-1 close
    html = re.sub(
        r'<button type="button" class="([^"]*?)close([^"]*?)"([^>]*)>\s*<span aria-hidden="true">&times;</span>\s*</button>',
        r'<button type="button" class="btn-close \1\2"\3></button>',
        html
    )
    return html


def replace_embed_responsive(html: str) -> str:
    """embed-responsive を ratio に置き換える。"""
    html = re.sub(
        r'<div class="embed-responsive embed-responsive-16by9">',
        '<div class="ratio ratio-16x9">',
        html
    )
    html = re.sub(r'\bembed-responsive-item\b', '', html)
    return html


def replace_btn_group_toggle(html: str) -> str:
    """btn-group-toggle / data-toggle="buttons" を BS5 の btn-check に置き換える。"""

    def convert_group(m):
        wrapper_class = m.group(1)  # "btn-group" or "btn-group-vertical"
        wrapper_attrs = m.group(2)  # remaining attrs on wrapper
        inner = m.group(3)

        # Determine input type from the first input found
        input_type_match = re.search(r'<input\s+type="(checkbox|radio)"', inner)
        if not input_type_match:
            # Regular buttons toggle group: keep wrapper, strip data-toggle,
            # add data-bs-toggle="button" to each button
            inner = re.sub(r'\s*data-toggle="buttons"', '', inner)
            inner = re.sub(
                r'<button\s+type="button"\s+class="([^"]*)"',
                r'<button type="button" class="\1" data-bs-toggle="button"',
                inner
            )
            return f'<div class="{wrapper_class}"{wrapper_attrs}>{inner}</div>'

        input_type = input_type_match.group(1)
        is_checkbox = input_type == "checkbox"

        # Parse each <label class="btn ...">...<input type=...>...</label> item
        # The label may contain an input and text.
        label_pattern = re.compile(
            r'<label\s+class="([^"]*btn[^"]*)"([^>]*)>(.*?)</label>',
            re.DOTALL
        )
        items = []
        counter = 1
        for lm in label_pattern.finditer(inner):
            label_classes = lm.group(1)
            label_attrs = lm.group(2)
            label_inner = lm.group(3)

            # Extract input attributes
            input_match = re.search(
                r'<input\s+type="' + input_type + r'"([^>]*?)>',
                label_inner
            )
            if not input_match:
                continue
            input_attrs = input_match.group(1)

            # Get text content after the input
            text = re.sub(r'<input[^>]*>', '', label_inner, count=1)
            text = re.sub(r'<\/?[^>]+>', '', text)  # strip any remaining tags
            text = ' '.join(text.split())  # normalize whitespace

            checked = 'checked' in input_attrs
            name_match = re.search(r'name="([^"]+)"', input_attrs)
            name = name_match.group(1) if name_match else (f'btn{input_type}' if not is_checkbox else '')
            id_match = re.search(r'id="([^"]+)"', input_attrs)
            base_id = id_match.group(1) if id_match else f'btn{input_type}{counter}'
            autocomplete = 'autocomplete="off"' if 'autocomplete="off"' in input_attrs else ''

            # Use BS5 conventional ids when none were provided
            if base_id == f'btn{input_type}{counter}':
                base_id = f'btncheck{counter}' if is_checkbox else f'btnradio{counter}'

            if is_checkbox:
                input_el = f'<input type="checkbox" class="btn-check" id="{base_id}" {autocomplete}{" checked" if checked else ""}>'
            else:
                input_el = f'<input type="radio" class="btn-check" name="{name}" id="{base_id}" {autocomplete}{" checked" if checked else ""}>'

            # Preserve button color classes (btn-primary, btn-secondary, etc.)
            btn_classes = ' '.join(c for c in label_classes.split() if c.startswith('btn-') or c == 'btn')
            if not btn_classes:
                btn_classes = 'btn btn-primary'

            items.append((input_el, btn_classes, base_id, text))
            counter += 1

        if not items:
            return m.group(0)

        # Build wrapper
        clean_wrapper_class = ' '.join(
            c for c in wrapper_class.split() if c != 'btn-group-toggle'
        )
        role_attr = 'role="group"'
        aria_label = f'aria-label="Basic {input_type} toggle button group"'
        wrapper = f'<div class="{clean_wrapper_class}" {role_attr} {aria_label}>'

        body = '\n'.join(
            f'            {it[0]}\n            <label class="{it[1]}" for="{it[2]}">{it[3]}</label>'
            for it in items
        )

        return f'{wrapper}\n{body}\n          </div>'

    # Match wrapper: btn-group btn-group-toggle or btn-group-vertical with data-toggle/data-bs-toggle="buttons"
    pattern = re.compile(
        r'<div\s+class="([^"]*?\b(?:btn-group|btn-group-vertical)\b[^"]*)"\s+data-(?:bs-)?toggle="buttons"([^>]*)>(.*?)</div>',
        re.DOTALL
    )
    html = pattern.sub(convert_group, html)
    return html


def add_form_labels(html: str) -> str:
    """BS5 では form-label クラスが推奨されるため、label に追加する。"""
    # <label for="..."> を <label class="form-label" for="..."> に
    # ただし既に class がある場合は form-label を追加（class 属性の位置は不問）
    # ボタンラベル（.btn を含む）や form-check-label には追加しない
    def repl(m):
        attrs = m.group(1)
        class_match = re.search(r'\sclass="([^"]*)"', attrs)
        if class_match:
            existing = class_match.group(1)
            if 'btn' in existing or 'form-check-label' in existing or 'form-label' in existing:
                return m.group(0)
            new_classes = (existing + ' form-label').strip()
            new_attrs = attrs.replace(class_match.group(0), f' class="{new_classes}"')
            return f'<label{new_attrs}>'
        else:
            return f'<label class="form-label"{attrs}>'

    html = re.sub(r'<label([^>]*)>', repl, html)
    return html


def add_nav_tab_roles(html: str) -> str:
    """nav-tabs のリンクに role="tab"、tab-pane に role="tabpanel" を追加する。"""
    # data-bs-toggle="tab" の a タグに role="tab" を追加
    html = re.sub(
        r'<a class="([^"]*?)" data-bs-toggle="tab" href="([^"]+)"',
        r'<a class="\1" data-bs-toggle="tab" href="\2" role="tab"',
        html
    )
    # tab-pane に role="tabpanel" を追加
    html = re.sub(
        r'<div class="tab-pane fade([^"]*)" id="([^"]+)">',
        r'<div class="tab-pane fade\1" id="\2" role="tabpanel">',
        html
    )
    return html


def fix_assets_paths(html: str, is_docs: bool = True) -> str:
    """CSS/JS のパスを本プロジェクト構成に合わせる。"""
    prefix = '../' if is_docs else ''
    html = re.sub(r'href="css/bootstrap\.css"', f'href="{prefix}dist/css/bootstrap.css"', html)
    html = re.sub(r'href="\.\/css/bootstrap\.css"', f'href="{prefix}dist/css/bootstrap.css"', html)
    html = re.sub(r'src="\.\/js/bootstrap\.min\.js"', 'src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"', html)
    # Popper は BS5 bundle に含まれるため削除。jQuery はサンプル内の
    # 初期化コードで使われているため残す。
    html = re.sub(
        r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/popper\.js/[^"]+"[^>]*></script>\s*',
        '',
        html
    )
    # index へのリンク
    html = re.sub(r'href="\./"', f'href="{prefix}index.html"', html)
    return html


def add_jumbotron_style(html: str) -> str:
    """<style> 内に .jumbotron の定義がなければ追加する。"""
    if '.jumbotron' in html:
        return html
    style_end = html.rfind('</style>')
    if style_end == -1:
        return html
    jumbotron_css = '''
  .jumbotron {
    padding: 4rem 2rem;
    margin-bottom: 2rem;
    background-color: #e9ecef;
    border-radius: .3rem;
  }
'''
    return html[:style_end] + jumbotron_css + html[style_end:]


def replace_bs5_popover_tooltip_init(html: str) -> str:
    """jQuery 形式の popover/tooltip 初期化を BS5 ネイティブに置き換える。"""
    legacy = r"""\$\('\.bs-component \[data-bs-toggle="popover"\]'\)\.popover\(\);\s*\$\('\.bs-component \[data-bs-toggle="tooltip"\]'\)\.tooltip\(\);"""
    native = """var popoverTriggerList = [].slice.call(document.querySelectorAll('.bs-component [data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  })
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('.bs-component [data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })"""
    html = re.sub(legacy, native, html)
    return html


def move_nav_item_active_to_link(html: str) -> str:
    """BS4 では .nav-item に付いていた active クラスを BS5 では .nav-link に移す。"""
    # <li class="nav-item active">...<a class="nav-link" ...>...</a>...</li>
    # → <li class="nav-item">...<a class="nav-link active" ...>...</a>...</li>
    def repl(m):
        item_classes = m.group(1)
        attrs_after_class = m.group(2)
        inner = m.group(3)
        # .nav-item から active を外す
        item_classes = re.sub(r'\s*\bactive\b', '', item_classes).strip()
        # 内側の最初の .nav-link に active を追加
        inner = re.sub(
            r'(<a\s+class="[^"]*?)\bnav-link\b([^"]*?")',
            r'\1nav-link active\2',
            inner,
            count=1
        )
        return f'<li class="{item_classes}"{attrs_after_class}>{inner}</li>'

    html = re.sub(
        r'<li class="([^"]*?\bnav-item\b[^"]*?\bactive\b[^"]*)"([^>]*)>((?:(?!<li[\s>]).)*?<a\s+class="[^"]*\bnav-link\b[^"]*"[^>]*>.*?</a>(?:(?!</li>).)*)</li>',
        repl,
        html,
        flags=re.DOTALL
    )
    return html


def remove_jquery_if_unused(html: str) -> str:
    """jQuery を使わないファイルでは jQuery の読み込みとその初期化コードを削除する。"""
    # 游ゴシック切り替えボタンが実際に HTML 内にあれば jQuery を残す
    has_yu_button = re.search(r'id=["\']anti-yu-gothic-button["\']', html) is not None
    if not has_yu_button:
        html = re.sub(
            r'<script src="https://code\.jquery\.com/jquery-[^"]+"[^>]*></script>\s*',
            '',
            html
        )
        # 游ゴシック切り替えの jQuery コードが残っていれば削除
        html = re.sub(
            r"\$\('#anti-yu-gothic-button'\)\.on\('click', function\(\) \{[\s\S]*?\}\);\s*",
            '',
            html
        )
    return html


def convert(html: str, is_docs: bool = True) -> str:
    html = fix_assets_paths(html, is_docs)
    html = replace_data_attrs(html)
    html = replace_utility_classes(html)
    html = replace_badges(html)
    html = replace_custom_forms(html)
    html = replace_input_group_addons(html)
    html = replace_custom_file(html)
    html = replace_close_buttons(html)
    html = replace_embed_responsive(html)
    html = replace_btn_group_toggle(html)
    html = add_form_labels(html)
    html = add_nav_tab_roles(html)
    html = add_jumbotron_style(html)
    html = replace_bs5_popover_tooltip_init(html)
    html = move_nav_item_active_to_link(html)
    html = remove_jquery_if_unused(html)
    return html


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <input.html> <output.html>')
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    html = input_path.read_text(encoding='utf-8')
    converted = convert(html, is_docs=True)
    output_path.write_text(converted, encoding='utf-8')
    print(f'Converted: {output_path}')


if __name__ == '__main__':
    main()
