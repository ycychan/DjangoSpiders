// author : dominoar
// date : 2022/10/31
// lasttime 2022/10/31
// version: 1.0
// Warring!

const search_input = $(".search-input-text .line-form-input");
let first_text = '';
let page_number = 1;

// 定义每一个资源的提取方式
const postsFunction = {
    lzacgsearch: function (json_data, i) {
        return $("<posts class=\"posts-item list ajax-item no_margin flex\"><div class=\"post-graphic\"><div class=\"item-thumbnail\"><a target=\"_blank\" href=" + json_data[i]['res_url'] + "><img data-thumb=\"default\" src=" + json_data[i]['res_img_url'] + " data-src=\"https://ycychan.com/wp-content/themes/action/../img/thumbnail.svg\" alt=" + json_data[i]['res_title'] + " class=\"fit-cover radius8 lazyloaded\"></a></div></div><div class=\"item-body flex xx flex1 jsb\"><h2 class=\"item-heading\"><a target=\"_blank\" href=" + json_data[i]['res_url'] + ">" + json_data[i]['res_title'] + "</a></h2><div class=\"item-excerpt muted-color text-ellipsis mb6\">?</div><div><div class=\"item-tags scroll-x no-scrollbar mb6\"><a class=\"but c-blue\" title=\"没有更多了\" href=\"javascript:;\"><i class=\"fa fa-folder-open-o\" aria-hidden=\"true\"></i>?</a></div><div class=\"item-meta muted-2-color flex jsb ac\"><item class=\"meta-author flex ac\"><a href=\"javascript:;\"><span class=\"avatar-mini\"><img alt=\"?\" src=\"\" data-src=\"//ycychan.com/wp-content/themes/action/../img/avatar-default.png\" class=\"avatar avatar-id-1 ls-is-cached lazyloaded\"></span></a><span class=\"hide-sm ml6\">dominaor</span><span title=\"2022-10-29 11:31:24\" class=\"icon-circle\">?</span></item><div class=\"meta-right\"><item class=\"meta-comm\"><a data-toggle=\"tooltip\" title=\"无评论\" href=" + json_data[i]['res_url'] + "><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-comment\"></use></svg>0</a></item><item class=\"meta-view\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-view\"></use></svg>6</item><item class=\"meta-like\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-like\"></use></svg>0</item></div></div></div></div></posts>");
    },
    dmhysearch: function () {
    }
}

// 页面加载完毕之后加载posts进入content中
$(function (e) {
    e.preventDefault();
    search_input.hide();
    let search_text = search_input.val();
    if (first_text !== search_text) {
        page_number = 1;
        first_text = search_text;
    }
    if (search_text !== '') {
        postsSpiderPost('lzacgsearch', search_text, page_number)
    }
});

// post封装
function postsSpiderPost(entrance, search_text, page_number = 1) {
    let x = false;
    $.ajax({
        type: "POST",
        url: "https://ycyspace.cn/" + entrance,
        data: JSON.stringify({'key': search_text, 'page': page_number}),
        datatype: "json",
        cache: false,
        success: function (resp) {
            console.log(resp);
            let json_data = resp;
            let div_search_content = $(".content-layout .search-content");
            for (let i = 0; i < json_data.length; i++) {
                div_search_content.append(postsFunction.lzacgsearch(json_data, i));
            }
            page_number++;
            search_input.show();
            x = true
        },
        error: function (resp) {
            search_input.show()
        }
    });
    return x;
}
