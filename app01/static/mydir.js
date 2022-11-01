// author : dominoar
// date : 2022/10/31
// lasttime 2022/10/31
// version: 1.0
// Warring!

const search_input_div = $(".search-input-text");
const search_input = $(".search-input-text .line-form-input");
const search_input_copy = search_input;
const search_form = $(".search-input .search-form");
let page_number = 1;
let first_text = '';


search_form.submit(function (e) {
    e.preventDefault();
    search_input.remove();
    let search_text = search_input.val();
    if (first_text !== search_text) {
        page_number = 1;
        first_text = search_text;
    }
    if (search_text !== '') {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/lzacgsearch",
            data: JSON.stringify({'key': search_text, 'page': page_number}),
            datatype: "json",
            cache: false,
            success: function (resp) {
                console.log(resp);
                let json_data = resp;
                let div_search_content = $(".content-layout .search-content");
                for (let i = 0; i < json_data.length; i++) {
                    let posts = $("<posts class=\"posts-item list ajax-item no_margin flex\"><div class=\"post-graphic\"><div class=\"item-thumbnail\"><a target=\"_blank\" href=" + json_data[i]['res_url'] + "><img data-thumb=\"default\" src=" + json_data[i]['res_img_url'] + " data-src=\"https://ycychan.com/wp-content/themes/action/../img/thumbnail.svg\" alt=" + json_data[i]['res_title'] + " class=\"fit-cover radius8 lazyloaded\"></a></div></div><div class=\"item-body flex xx flex1 jsb\"><h2 class=\"item-heading\"><a target=\"_blank\" href=" + json_data[i]['res_url'] + ">" + json_data[i]['res_title'] + "</a></h2><div class=\"item-excerpt muted-color text-ellipsis mb6\">?</div><div><div class=\"item-tags scroll-x no-scrollbar mb6\"><a class=\"but c-blue\" title=\"没有更多了\" href=\"javascript:;\"><i class=\"fa fa-folder-open-o\" aria-hidden=\"true\"></i>?</a></div><div class=\"item-meta muted-2-color flex jsb ac\"><item class=\"meta-author flex ac\"><a href=\"javascript:;\"><span class=\"avatar-mini\"><img alt=\"?\" src=\"\" data-src=\"//ycychan.com/wp-content/themes/action/../img/avatar-default.png\" class=\"avatar avatar-id-1 ls-is-cached lazyloaded\"></span></a><span class=\"hide-sm ml6\">dominaor</span><span title=\"2022-10-29 11:31:24\" class=\"icon-circle\">?</span></item><div class=\"meta-right\"><item class=\"meta-comm\"><a data-toggle=\"tooltip\" title=\"无评论\" href=" + json_data[i]['res_url'] + "><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-comment\"></use></svg>0</a></item><item class=\"meta-view\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-view\"></use></svg>6</item><item class=\"meta-like\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-like\"></use></svg>0</item></div></div></div></div></posts>");
                    div_search_content.append(posts);
                }
                page_number++;
                search_input_div.prepend(search_input_copy);
            },
            error: function (resp) {
                search_input_div.prepend(search_input_copy);
            }
        });
    }

});