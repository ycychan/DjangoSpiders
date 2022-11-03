// author : dominoar
// date : 2022/10/31
// lasttime 2022/11/2
// version: 1.0
// Warring!

const div_search_content = $(".content-layout .search-content");
const home_posts_raw = $('#index-tab-main')
const self_url = window.location.href;
const search_input = $(".search-input-text .line-form-input");
const search_form = $(".search-form");
let first_text = '';
let page_number = 1;

// 定义每一个资源的提取方式
const postsFunction = {
    'lzacgsearch': function (json_data) {
        div_search_content.append($("<posts class=\"posts-item list ajax-item no_margin flex\"><div class=\"post-graphic\"><div class=\"item-thumbnail\"><a target=\"_blank\" href=" + json_data['res_url'] + "><img data-thumb=\"default\" src=" + json_data['res_img_url'] + " data-src=\"https://ycychan.com/wp-content/themes/action/../img/thumbnail.svg\" alt=" + json_data['res_title'] + " class=\"fit-cover radius8 lazyloaded\"></a></div></div><div class=\"item-body flex xx flex1 jsb\"><h2 class=\"item-heading\"><a target=\"_blank\" href=" + json_data['res_url'] + ">" + json_data['res_title'] + "</a></h2><div class=\"item-excerpt muted-color text-ellipsis mb6\">-</div><div><div class=\"item-tags scroll-x no-scrollbar mb6\"><a class=\"but c-blue\" title=\"没有更多了\" href=\"javascript:;\"><i class=\"fa fa-folder-open-o\" aria-hidden=\"true\"></i>-</a></div><div class=\"item-meta muted-2-color flex jsb ac\"><item class=\"meta-author flex ac\"><a href=\"javascript:;\"><span class=\"avatar-mini\"><img alt=\"-\" src=\"\" data-src=\"//ycychan.com/wp-content/themes/action/../img/avatar-default.png\" class=\"avatar avatar-id-1 ls-is-cached lazyloaded\"></span></a><span class=\"hide-sm ml6\">-</span><span title=\"-\" class=\"icon-circle\">-</span></item><div class=\"meta-right\"><item class=\"meta-comm\"><a data-toggle=\"tooltip\" title=\"-\" href=" + json_data['res_url'] + "><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-comment\"></use></svg>-</a></item><item class=\"meta-view\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-view\"></use></svg>-</item><item class=\"meta-like\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-like\"></use></svg>-</item></div></div></div></div></posts>"));
    },
    'lzacghome': function (json_data) {
        home_posts_raw.append($('<posts class="posts-item ajax-item card"><div class="item-thumbnail"><a target="_blank" href="' + json_data['res_url'] + '"><img src="' + json_data['res_img_url'] + '" alt="' + json_data['res_title'] + '" class="fit-cover radius8"></a></div><div class="item-body"><h2 class="item-heading"><a target="_blank" href="' + json_data['res_url'] + '">' + json_data['res_title'] + '</a></h2><div class="item-tags scroll-x no-scrollbar mb6"><a href="https://lzacg.one/tag/' + json_data['res_author'] + '" title="查看此标签更多文章" class="but"># ' + json_data['res_author'] + '</a></div><div class="item-meta muted-2-color flex jsb ac"><item title="' + json_data['res_send_time'] + '" class="icon-circle mln3">' + json_data['res_send_time'] + '</item><div class="meta-right"><item class="meta-comm"><a data-toggle="tooltip" title="" href="' + json_data['res_url'] + '#comments" data-original-title="去评论"><svg class="icon" aria-hidden="true"><use xlink:href="#icon-comment"></use></svg>3</a></item><item class="meta-view"><svg class="icon" aria-hidden="true"><use xlink:href="#icon-view"></use></svg>2805</item></div></div></div></posts>'));
    },
    'dmhysearch': function (json_data) {
        div_search_content.append($("<posts class=\"posts-item list ajax-item no_margin flex\"><div class=\"post-graphic\"><div class=\"item-thumbnail\"><a target=\"_blank\" href=" + json_data['res_url'] + "><img data-thumb=\"default\" src=" + 'javascript:;' + " data-src=\"https://ycychan.com/wp-content/themes/action/../img/thumbnail.svg\" alt=" + json_data['title'] + " class=\"fit-cover radius8 lazyloaded\"></a></div></div><div class=\"item-body flex xx flex1 jsb\"><h2 class=\"item-heading\"><a target=\"_blank\" href=" + json_data['res_url'] + ">" + json_data['title'] + "</a></h2><div class=\"item-excerpt muted-color text-ellipsis mb6\">-</div><div><div class=\"item-tags scroll-x no-scrollbar mb6\"><a class=\"but c-blue\" title=\"无分类\" href=" + json_data['res_publisher_url'] + "><i class=\"fa fa-folder-open-o\" aria-hidden=\"true\"></i>" + json_data['res_publisher'] + "</a></div><div class=\"item-meta muted-2-color flex jsb ac\"><item class=\"meta-author flex ac\"><a href=" + json_data['res_group_url'] + "><span class=\"avatar-mini\"><img alt=\"-\" src=\"\" data-src=\"//ycychan.com/wp-content/themes/action/../img/avatar-default.png\" class=\"avatar avatar-id-1 ls-is-cached lazyloaded\"></span></a><span class=\"hide-sm ml6\">" + json_data['res_group'] + "</   span><span title=" + json_data['send_time'] + " class=\"icon-circle\">" + json_data['res_type'] + "</span></item><div class=\"meta-right\"><item class=\"meta-comm\"><a data-toggle=\"tooltip\" title=\"-\" href=" + json_data['res_url'] + "><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-comment\"></use></svg>-</a></item><item class=\"meta-view\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-view\"></use></svg>6</item><item class=\"meta-like\"><svg class=\"icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-like\"></use></svg>-</item></div></div></div></div></posts>"));
    },
    'dmhyhome': function (json_data) {
        home_posts_raw.append($('<posts class="posts-item ajax-item card"><div class="item-thumbnail"><a target="_blank" href="' + json_data['res_url'] + '"><img src="' + json_data['res_img_url'] + '" alt="' + json_data['res_title'] + '" class="fit-cover radius8"></a></div><div class="item-body"><h2 class="item-heading"><a target="_blank" href="' + json_data['res_url'] + '">' + json_data['res_title'] + '</a></h2><div class="item-tags scroll-x no-scrollbar mb6"><a href="' + json_data['res_author'] + '" title="查看此作者更多资源" class="but"># ' + json_data['res_author'] + '</a></div><div class="item-meta muted-2-color flex jsb ac"><item title="' + json_data['res_send_time'] + '" class="icon-circle mln3">' + json_data['res_send_time_text'] + '</item><div class="meta-right"><item class="meta-comm"><a data-toggle="tooltip" title="" href="' + json_data['res_magent'] + '" data-original-title="种子直链"><svg class="icon" aria-hidden="true"><use xlink:href="#icon-comment"></use></svg>种子</a></item><item class="meta-view"><svg class="icon" aria-hidden="true"><use xlink:href="#icon-view"></use></svg>2805</item></div></div></div></posts>'));
    }
}

// 页面加载完毕之后加载posts进入content中
$(function (e) {
    search_input.hide();
    let search_text = search_input.val();
    if (first_text !== search_text) {
        page_number = 1;
        first_text = search_text;
    }
    if (search_text !== '') {
        postsSpiderPost('lzacgsearch', search_text, page_number);
        postsSpiderPost('dmhysearch', search_text, page_number);
    } else {
        postsSpiderPost('lzacghome')
        postsSpiderPost('dmhyhome')
    }
    search_input.show();
});

// post
function postsSpiderPost(entrance, search_text = '', page_number = 1) {
    let x = false;
    $.ajax({
        type: "POST",
        url: "https://ycyspace.cn/" + entrance,
        data: JSON.stringify({ 'key': search_text, 'page': page_number }),
        datatype: "json",
        cache: false,
        success: function (resp) {
            console.log(resp);
            let json_data = resp;
            for (let i = 0; i < json_data.length; i++) {
                postsFunction[entrance](json_data[i], i);
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
