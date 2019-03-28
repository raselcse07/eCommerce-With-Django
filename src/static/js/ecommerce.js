$(document).ready(function(){
        // Auto Search
        var searchForm = $(".search-form")
        var searchInput = searchForm.find("[name='q']")
        var typingTimer;
        var typingInterval = 500 // .5 seconds
        var searchBtn = searchForm.find("[type='submit']")

        searchInput.keyup(function(event){
            // key released
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch,typingInterval)
        })

        searchInput.keydown(function(event){
            // key pressed
            clearTimeout(typingTimer)
        })
        
        function do_search(){
          searchBtn.addClass("disabled")
          searchBtn.html("<i class='fas fa-spin fa-spinner'></i> Searching ...")
        }

        function performSearch(){
          do_search()
          var query = searchInput.val()
          setTimeout(function(){
            window.location.href = "/search/?q=" + query
          },1000)
        }
        
        // Cart + Add Product
        var productForm = $(".product-ajax")
        productForm.submit(function(event){
          event.preventDefault();
          var thisForm = $(this);
          // var actionEndPoint = thisForm.attr("action");
          var actionEndPoint = thisForm.attr("data-endpoint");
          var httpMethod = thisForm.attr("method");
          var formData = thisForm.serialize();

          $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function(data){
              submit_span = thisForm.find(".submit-span")
              if (data.added){
                  submit_span.html("<button class='btn btn-danger' type='submit'>Remove</button>")
              } else {
                  submit_span.html(" <button class='btn btn-success' type='submit'>Add to Cart</button>")
              }
              var navBarCount = $(".cart-count")
              var currentCartPath = window.location.href
              navBarCount.text(data.cart_item_count)
              if (currentCartPath.indexOf('cart') != -1){
                updateCart()
              }
            },
            error: function(errorData){
              $.alert({
                  title:"Oops!",
                  content:"An error ocured.",
                  theme:"modern",
                })
            }
          })

          function updateCart(){
            var cartTable = $(".cart-table")
            var cartBody = cartTable.find(".cart-body")
            var productRow = cartBody.find(".cart-product")
            var currentCartUrl = window.location.href

            var refreshCartUrl = "/cart/api/";
            var updateCartMethod = "GET";
            var data = {};

            $.ajax({
              url: refreshCartUrl,
              method: updateCartMethod,
              data: data,
              success:function(data){
                  var hoddenCartRemoveForm = $(".cart-item-remove-form")
                  if (data.product.length > 0){
                    productRow.html(" ")
                    i = data.product.length
                    $.each(data.product, function(index,value){
                        var newCartItemRemove = hoddenCartRemoveForm.clone()
                        newCartItemRemove.css("display","block")
                        newCartItemRemove.find(".cart-product-id").val(value.id)
                        cartBody.prepend("<tr> <th scope='row'>" + i + "</th><td><a href='" + value.url +"'>" + value.title + "</a>"+ newCartItemRemove.html() +"</td><td>" + value.price + "</td></tr>")
                        i --
                      })
                    cartBody.find(".cart-subtotal").text(data.sub_total)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                  window.location.href = currentCartUrl
                }
              },
              error:function(errorData){
                $.alert({
                  title:"Oops!",
                  content:"An error ocured.",
                  theme:"modern",
                })
              }
            })
          }
      })
  })