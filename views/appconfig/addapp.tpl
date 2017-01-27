%include('header')

<script>
$(document).ready(function () {
    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();
    
    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

        var $target = $(e.target);
    
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);

    });
    $(".prev-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });
});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

function checkApp(appname) {
   jQuery.ajax({
      type: "POST",
      url:  "/app_exists/"+appname,
      data: { appname: appname },
      complete: function(xhr){
         var response = eval(xhr.responseText);
         if (response) {
            $("#appname").toggleClass('has-error', true);
            $("#appname").toggleClass('has-success', false);
            $("#appname").select()
            $("#helper").removeClass('hidden');
            $("#feedback").removeClass('glyphicon-ok')
            $("#feedback").addClass('glyphicon-remove')
            $("#submit").prop('disabled',true)
         } else {
            $("#appname").toggleClass('has-error', false);
            $("#appname").toggleClass('has-success', true);
            $("#helper").addClass('hidden');
            $("#feedback").addClass('glyphicon-ok')
            $("#feedback").removeClass('glyphicon-remove')
            $("#command").val("../../../../apps/"+appname+"/"+appname)
            $("#submit").prop('disabled',false)
         }
      }
   })
}
</script>

<style>
i {
    padding: 20px;
}

.wizard {
    margin: 20px auto;
    background: #fff;
}

.wizard .nav-tabs {
    position: relative;
    margin: 40px auto;
    margin-bottom: 0;
    border-bottom-color: #e0e0e0;
}

.wizard > div.wizard-inner {
    position: relative;
}

.connecting-line {
    height: 2px;
    background: #e0e0e0;
    position: absolute;
    width: 80%;
    margin: 0 auto;
    left: 0;
    right: 0;
    top: 50%;
    z-index: 1;
}

.wizard .nav-tabs > li.active > a, .wizard .nav-tabs > li.active > a:hover, .wizard .nav-tabs > li.active > a:focus {
    color: #555555;
    cursor: default;
    border: 0;
    border-bottom-color: transparent;
}

span.round-tab {
    width: 70px;
    height: 70px;
    line-height: 70px;
    display: inline-block;
    border-radius: 100px;
    background: #fff;
    border: 2px solid #e0e0e0;
    z-index: 2;
    position: absolute;
    left: 0;
    text-align: center;
    font-size: 25px;
}
span.round-tab i{
    color:#555555;
}
.wizard li.active span.round-tab {
    background: #fff;
    border: 2px solid #5bc0de;
    
}
.wizard li.active span.round-tab i{
    color: #5bc0de;
}

span.round-tab:hover {
    color: #333;
    border: 2px solid #333;
}

.wizard .nav-tabs > li {
    width: 25%;
}

.wizard li:after {
    content: " ";
    position: absolute;
    left: 46%;
    opacity: 0;
    margin: 0 auto;
    bottom: 0px;
    border: 5px solid transparent;
    border-bottom-color: #5bc0de;
    transition: 0.1s ease-in-out;
}

.wizard li.active:after {
    content: " ";
    position: absolute;
    left: 46%;
    opacity: 1;
    margin: 0 auto;
    bottom: 0px;
    border: 10px solid transparent;
    border-bottom-color: #5bc0de;
}

.wizard .nav-tabs > li a {
    width: 70px;
    height: 70px;
    margin: 20px auto;
    border-radius: 100%;
    padding: 0;
}

    .wizard .nav-tabs > li a:hover {
        background: transparent;
    }

.wizard .tab-pane {
    position: relative;
    padding-top: 50px;
}

.wizard h3 {
    margin-top: 0;
}

@media( max-width : 585px ) {

    .wizard {
        width: 90%;
        height: auto !important;
    }

    span.round-tab {
        font-size: 16px;
        width: 50px;
        height: 50px;
        line-height: 50px;
    }

    .wizard .nav-tabs > li a {
        width: 50px;
        height: 50px;
        line-height: 50px;
    }

    .wizard li.active:after {
        content: " ";
        position: absolute;
        left: 35%;
    }
}
</style>
</head>
<body>
%include('navbar')

<div class="container">
    <div class="row">
        <section>
        <div class="wizard">
            <div class="wizard-inner">
                <div class="connecting-line"></div>
                <ul class="nav nav-tabs" role="tablist">

                    <li role="presentation" class="active">
                        <a href="#step1" data-toggle="tab" aria-controls="step1" role="tab" title="Step 1">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-folder-open"></i>
                            </span>
                        </a>

                    </li>

                    <li role="presentation" class="disabled">
                        <a href="#step2" data-toggle="tab" aria-controls="step2" role="tab" title="Step 2">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-pencil"></i>
                            </span>
                        </a>
                    </li>
                    <!-- <li role="presentation" class="disabled">
                        <a href="#step3" data-toggle="tab" aria-controls="step3" role="tab" title="Step 3">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-picture"></i>
                            </span>
                        </a>
                    </li> -->

                    <li role="presentation" class="disabled">
                        <a href="#complete" data-toggle="tab" aria-controls="complete" role="tab" title="Complete">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-ok"></i>
                            </span>
                        </a>
                    </li>
                </ul>
            </div>

            <form action="/addapp" method="post">

            <div class="tab-content">
                <div class="tab-pane active" role="tabpanel" id="step1">
                    <h3>Step 1</h3>

                    <div id="appname" class="form-group has-feedback">
                        <label for="appname" style="text-align:right" class="control-label col-xs-6">Name of app:</label>
                        <div class="col-xs-6">
                            <input type="text" class="form-control input-lg"  
                                   name="appname" onchange="checkApp(this.value)"><br>
                            <span id="feedback" style="right:20px" class="glyphicon form-control-feedback"></span>
                            <span id="helper" class="help-block hidden">App name is already taken. Try another name.</span>
                        </div>
                    </div>

                    <ul class="list-inline pull-right">
                        <li><button type="button" class="btn btn-success next-step">Save and continue</button></li>
                    </ul>
                </div>

                <div class="tab-pane" role="tabpanel" id="step2">
                    <h3>Step 2</h3>
                    <p>Configure App</p>
                    <form class="form-horizontal" action="/addapp/step2" method="post">
                    <!-- <input type="hidden" name="appname" value="{appname}">
                    <input type="hidden" name="user" value="{user}"> -->

                    <table>
                    <tr>
                    <td><font size="+1">Description:<br>
                        <font size="-1">80 chars max</font></font></td>
                    <td><textarea class="form-control" name="description" cols=40 rows=2></textarea></td>

                    <!-- <tr>
                    <td><font size="+1">Tags:</font><br>
                        <font size="-1">e.g. Bioinformatics</font></td>
                    <td><input class="form-control" id="category" name="category" data-role="tagsinput" type="text" ></td> -->

                    <!--
                    <td><select name="category" onchange="somefn()">
                       <option SELECTED value="bioinformatics">Bioinformatics
                       <option value="bioinformatics">Bioinformatics
                       <option value="cfd">CFD
                       <option value="other">Other
                    </select></td>
                    -->
                    </tr>

                    <!--
                    <tr>
                    <td>Language:</td>
                    <td><select name="language">
                       <option value="c">c
                       <option value="C++">C++
                       <option value="fortran">Fortran
                       <option value="fortran">Fortran90
                       <option value="java">Java
                       <option SELECTED value="python">Python
                       <option value="ruby">Ruby
                    </select></td>
                    </tr>
                    -->

                    <tr>
                    <td><font size="+1">Input format:</font></td>
                    <td>
                        %input_format = "INI"
                        %include('appconfig/input_opts')
                    </td>
                    </tr>

                    <tr>
                    <td><font size="+1">Command to run app:</font><br> 
                    <font size="-1">Note: this is a relative path from the <tt>user_data/app/user</tt> directory</font></td>
                    <td><input class="form-control" type="text" id="command" name="command"></td>
                    </tr>

                    </table>

                    <!--
                    <tr>
                    <td>Preprocess:</td>
                    <td><select name="preprocess">
                       <option SELECTED value="">None
                       <option value="1">Convert params to command line args
                    </select></td>
                    </tr>

                    <tr>
                    <td>Postprocess:</td>
                    <td><select name="postprocess">
                       <option SELECTED value="">None
                    </select></td>
                    </tr>
                    -->
                    </form>

                    <ul class="list-inline pull-right">
                        <li><button type="button" class="btn btn-link prev-step"><span class="glyphicon glyphicon-chevron-left"></span> Previous</button></li>
                        <li><button type="button" class="btn btn-success next-step">Save and continue</button></li>
                    </ul>
                </div>

                <div class="tab-pane" role="tabpanel" id="complete">
                    <h3>Complete</h3>
                    <p>Now we will submit this information to the server.</p>

                    <ul class="list-inline pull-right">
                        <li><button type="button" class="btn btn-link prev-step"><span class="glyphicon glyphicon-chevron-left"></span> Previous</button></li>
                        <input type="submit" class="btn btn-success btn-info-full next-step" value="Submit">
                    </ul>

                </div>
                <div class="clearfix"></div>
            </div>
            </form>

        </div>

    </section>
   </div>
</div>

</body>
</html>


