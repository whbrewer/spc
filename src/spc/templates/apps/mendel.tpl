{% include "header.tpl" %}

<script type="text/javascript" src="/static/apps/mendel/mendel.js"></script>
<style>
  .form-horizontal .control-label{
    text-align:left;
  }

  .tab-content {
    background-color: #fff;
    border: 1px solid #ddd;
    padding: 10px;
  }

  body {
    background: #f5f5f5 !important;
  }

  label {
      /*font-weight: normal !important;*/
      /*font-size: 120%;*/
  }

  a { text-decoration: none !important }
  label > a { color:MidnightBlue !important }
  label > a:hover { color:OrangeRed !important; cursor: pointer !important }
</style>
</head>

{% include "navbar.tpl" %}
{% include "apps/alert.tpl" %}
<div id="memory" align="center" class="alert-info hidden-xs"></div>
<div id="danger" align="center" class="alert-danger"></div>
<div id="warning" align="center" class="alert-warning"></div>

<body>

<div class="container-fluid">

<form role="form" class="form-horizontal" name="mendel_input"
      method="post" action="/confirm" novalidate>
<input type="hidden" name="app" value="{{app}}">
<input type="hidden" name="cid" value="{{cid}}">

<div class="col-sm-12 hidden-xs" style="height:5px"></div>
<div class="visible-xs" style="height:10px"></div>

<div class="row">
    <div class="hidden-xs col-sm-2">
      <button type="submit" class="btn btn-success" style="position:fixed; top: 8px; left: 530px; z-index:9999"> <!-- pull-right -->
        Continue <em class="glyphicon glyphicon-forward"></em> </button>
    </div>
</div>

<div class="tribe" id="tribediv" style="display:none">
  Tribe:
  <select class="form-control" name="tribe_id">
     <option VALUE=".001">.001</option>
     <option VALUE=".002">.002</option>
  </select>
</div>

<a target="_blank" href="/static/apps/mendel/help.html" class="help btn btn-info" ><span class="glyphicon glyphicon-question-sign"></span></a>
<!-- data-toggle="modal" data-target="#myModal" -->
<div>

  <!-- Nav tabs -->
  <!--<ul class="nav nav-tabs" role="tablist">-->
  <ul class="nav nav-pills" role="tablist">
    <li role="presentation" class="active"><a href="#basic" aria-controls="home" role="tab"    data-toggle="tab">Basic</a></li>
    <li role="presentation"><a href="#mutation" aria-controls="profile" role="tab"
        data-toggle="tab">Mutation</a></li>
    <li role="presentation"><a href="#selection" aria-controls="messages" role="tab"
        data-toggle="tab">Selection</a></li>
    <li role="presentation"><a href="#population" aria-controls="settings" role="tab"
        data-toggle="tab">Population</a></li>
    <li role="presentation"><a href="#substructure" aria-controls="settings" role="tab"
        data-toggle="tab">Substructure</a></li>
    <li role="presentation"><a href="#computation" aria-controls="settings" role="tab"
        data-toggle="tab">Computation</a></li>
    <li role="presentation"><a href="#special" aria-controls="settings" role="tab"
        data-toggle="tab">Special Applications</a></li>
  </ul>

  <!--*************************** BASIC TAB *******************************-->
  <div class="tab-content">
    <div role="tabpanel" class="tab-pane fade in active" id="basic">
      <div id="mutn_rate" class="form-group">
        <label for="mutn_rate" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="mutn_rate" data-content="This is the average number of new mutations per individual. In humans, this number is believed to be approximately 100. The mutation rate can be adjusted to be proportional to the size of the functional genome. Thus if only 10% of the human genome actually functions (assuming the rest to be biologically inert), then the biologically relevant mutation rate would be just 10. Rates of less than 1 new mutation per individual are allowed—including zero. The human default value is 10 new mutations per individual per generation.">1. Total non-neutral mutation rate:<br>
             &nbsp;&nbsp;&nbsp; (per individual per generation)</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" id="mutn_rate" name="mutn_rate"
                 value="{{mutn_rate}}" class="form-control"
                 min="0" max="10000" step="1"
                 onchange="compute_u(); fxn_auto_malloc(); validate(this)"
                 title="0 - 10,000; can be fraction e.g. 0.5">
        </div>
      </div>
      <div class="form-group">
        <label for="frac_fav_mutn" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="frac_fav_mutn" data-content="While some sources suggest this number might be as high as 1:1000, most sources suggest it is more realistically about 1:1,000,000. The default setting is 1:10,000. For studying the accumulation of only deleterious or only beneficial mutations, the number of beneficials can be set to zero or one.">2. Beneficial/deleterious ratio within non-neutral mutations:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" id="frac_fav_mutn" name="frac_fav_mutn"
                 value="{{frac_fav_mutn}}" class="form-control"
                 min="0.0" max="1.0" step="0.01"
                 onchange="compute_u(); fxn_auto_malloc(); validate(this)"
                 title="0.0 - 1.0 (e.g. if 1:1000, enter 0.001)">
          <table class="table">
            <tr><td>beneficial mutation rate: </td> <td><code><span id="uben"></span></code></td></tr>
            <tr><td>deleterious mutation rate:</td> <td><code><span id="udel"></span></font></code></td></tr>
          </table>
        </div>
      </div>

      <div class="form-group">
        <label id="pgr_label" for="reproductive_rate" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="reproductive_rate" data-content="This is the number of offspring per reproducing individual. Since population size in Mendel is usually constant, this variable defines the maximum amount of selection. There must be an average of at least one offspring per individual (after the selection process) for the population to maintain its size and avoid rapid extinction. Except where random death is considered, the entire surplus population is removed based upon phenotypic selection. The default value for humans is two offspring per selected individual (or four offspring per reproducing female).">3. Reproductive rate:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" class="form-control" id="reproductive_rate"
                 name="reproductive_rate" value="{{reproductive_rate}}"
                 onchange="fxn_auto_malloc(); validate(this)"
                 min="1" max="6" step="1">
        </div>
      </div>
      <div class="form-group">
        <label id="pop_size_label" for="pop_size" class="control-label col-xs-12 col-sm-6">
            <a data-toggle="popover" data-placement="right" title="pop_size" data-content="This is the number of reproducing adults, after selection. For parallel runs, this is the population size of each sub-population. This number is normally kept constant, except where fertility is insufficient to allow replacement, or where certain advanced parameters are used. For smaller computer systems such as PCs, population size must remain small (100-1000) or the program will quickly run out of memory. The default value is 1,000, since population sizes smaller than this can be strongly affected by inbreeding and drift. We find increasing population size beyond 1000 results in rapidly diminishing selective benefit.">4. Population size (per subpopulation):</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" id="pop_size" name="pop_size" data-warning="1000"
                   value="{{pop_size}}" class="form-control"
                   onchange="fxn_auto_malloc(); validate(this)"
                   min="2" max="2000" step="1" title="2 - 5,000">
          </div>
      </div>
      <div class="form-group">
        <label id="gen_label" for="num_generations" class="control-label col-xs-12 col-sm-6">
            <a data-toggle="popover" title="num_generations" data-content="The number of generations the program should run. The default is 500 generations. If there are too many generations specified, smaller computers will run out of memory because of the accumulation of large numbers of mutations, and the experiment will terminate prematurely. This problem can be mitigated by tracking only the larger-effect mutations (see advanced computation parameters).  The program also terminates prematurely if fitness reaches a specified extinction threshold (default = 0.0) or if the population size shrinks to just one individual.">5. Generations:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" id="num_generations" name="num_generations"
                 min="1" max="20000" step="100" data-warning="10000"
                 onchange="fxn_auto_malloc(); validate(this)"
                 class="form-control" value="{{num_generations}}" title="1 - 100,000">
        </div>
      </div>
    </div>

    <!--*************************** MUTATION TAB *******************************-->
    <div role="tabpanel" class="tab-pane fade" id="mutation">
      <div class="form-group">
        <label for="fitness_distrib_type" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="fitness_distrib_type" data-html="true" data-content='Deleterious mutations in the natural world typically range from a few rare lethals to a large number of nearly-neutral and neutral mutations. It is widely agreed that the distribution of mutational effects is characterized by an exponential-like function, where there are few high-impact mutations and many mutations which are nearly-neutral.  Mendel uses a generalized exponential function, called the Weibull function, to generate its distribution of mutation effects ranging from 1 (lethal) down to nearly 0 (near-neutral). <a target="_blank" href="/static/apps/mendel/help.html#psddme">Read more...</a>'>1. Distribution type:</a></label>
        <div class="col-xs-12 col-sm-3">
          <select id="fitness_distrib_type" name="fitness_distrib_type"
                  class="form-control"
                  onchange="fxn_fitness_distrib_type_change();">
          %opts = {'1': 'Natural distribution (Weibull)', '0': 'All mutations equal'}
          %for key, value in sorted(opts.items()):
            %if key == fitness_distrib_type:
              <option selected value="{{key}}">{{value}}
            %else:
              <option value="{{key}}">{{value}}
            %end
          %end
          </select>
        </div>
      </div>

      <div id="ufe_div" style="display:none">

        <div class="form-group">
          <label for="uniform_fitness_effect_del" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="uniform_fitness_effect_del" data-html="true" data-content='each deleterious mutation has exactly the same effect on fitness'>a. equal effect for each deleterious mutation:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="uniform_fitness_effect_del" class="form-control"
                   min="0" max="0.1" step="0.001" title="0 - 0.1" onchange="validate(this)"
                   value="{{uniform_fitness_effect_del}}">
          </div>
        </div>

        <div class="form-group">
          <label for="uniform_fitness_effect_fav" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="uniform_fitness_effect_fav" data-html="true" data-content='each favorable mutation has exactly the same effect on fitness'>b. equal effect for each beneficial mutation:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="uniform_fitness_effect_fav" class="form-control"
                   min="0" max="0.1" step="0.0001" title="0 - 0.1" onchange="validate(this)"
                   value="{{uniform_fitness_effect_fav}}">
          </div>
        </div>

      </div>

      <div id="weibull_div" style="display:none">

        <div class="form-group">
          <label class="control-label col-xs-12">
            &nbsp;&nbsp;&nbsp;
            Parameters shaping Weibull distribution of mutation effects:</label>
        </div>

        <div class="form-group">
          <label for="genome_size" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="genome_size" data-html="true" data-content='The distribution of deleterious mutational effects must in some way be adjusted to account for genome size. An approximate yet reasonable means for doing this is to define the minimal mutational effect as being 1 divided by the functional haploid genome size. The result of this adjustment is that smaller genomes have “flatter” distributions of deleterious mutations, while larger genomes have “steeper” distribution curves. Because we consider all entirely neutral mutations separately, we only consider the size of the functional genome, so we choose the default genome size to be 300 million (10% of the actual human genome size). <a target="_blank" href="/static/apps/mendel/help.html#hgs">Read more...</a>'>a. functional genome size:</a><br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <font size="-1">&rarr; G<sub>functional</sub> =
              G<sub>actual</sub> - G<sub>junk</sub></font> </label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="genome_size" id="hgs" accesskey="1"
                   value="{{genome_size}}" class="form-control"
                   min="100" max="1e11" step="1000" onchange="validate(this)"
                   title="100 - 100 billion">
          </div>
        </div>

        <div class="form-group">
          <label for="high_impact_mutn_fraction" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="high_impact_mutn_fraction" data-html="true" data-content='Most mutations have an effect on fitness that is too small to measure directly. However, mutations will have measurable effects in the far “tail” of the mutation distribution curve. By utilizing the frequency and distribution of “measurable” mutation effects, one can constrain the most significant portion of the distribution curve as it relates to the selection process. For most species, there may not yet be enough data, even for the major mutations, to accurately model the exact distribution of mutations. When such data is not yet available, we are forced to simply estimate, to the best of our ability and based on data from other organisms, the fraction of “major mutations”.  The human default is 0.001.'>b. fraction of del. mutations with "major effect":</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="high_impact_mutn_fraction"
                   value="{{high_impact_mutn_fraction}}" class="form-control"
                   min="0.0001" max="0.9" step="0.0001" title="0.0001 - 0.9"
                   onchange="validate(this)">
          </div>
        </div>

        <div class="form-group">
          <label for="high_impact_mutn_threshold" class="control-label col-xs-12 col-sm-6">
                &nbsp;&nbsp;&nbsp;
                <a data-toggle="popover" title="high_impact_mutn_threshold" data-content="A somewhat arbitrary level must be selected for defining what constitutes a “measurable”, or “major”, mutation effect. MENDEL uses a default value for this cut-off of 0.10. This is because under realistic clinical conditions, it is questionable that we can reliably measure a single mutation’s fitness effect when it changes fitness by less than 10%.">
                c. minimum del. effect defined as "major":</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="high_impact_mutn_threshold"
                   value="{{high_impact_mutn_threshold}}" class="form-control"
                   min="0.01" max="0.9" step="0.01" title="0.01 - 0.9"
                   onchange="validate(this)">
          </div>
        </div>

        <div class="form-group">
          <label for="max_fav_fitness_gain" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="max_fav_fitness_gain" data-html="true" data-content='A realistic upper limit must be placed upon beneficial mutations. This is because a single nucleotide change can expand total biological functionality of an organism only to a limited degree. The larger the genome and the greater the total genomic information, the less a single nucleotide is likely to increase the total. Researchers must make a judgment for themselves of what is a reasonable maximal value for a single base change. The MENDEL default value for this limit is 0.01. This limit implies that a single point mutation can increase total biological functionality by as much as 1%. <a target="_blank" href="/static/apps/mendel/help.html#rdbm">Read more...</a>'>d. maximum beneficial fitness effect:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="max_fav_fitness_gain" accesskey="2"
                   class="form-control" value="{{max_fav_fitness_gain}}"
                   min="0.000001" step="0.000001" title="0.000001 - nolimit"
                   onchange="validate(this)">
          </div>
        </div>

        <input type="hidden" name="num_initial_fav_mutn" value="{{num_initial_fav_mutn}}">

      </div> <!-- weibull_div -->

      <hr>

      <div class="form-group">
        <label class="control-label col-xs-12">
          <a data-toggle="popover" title="dominant vs. recessive" data-content="It is widely agreed that in diploid species, most mutations are recessive, while a small fraction are dominant. In the case of co-dominance, all mutations behave additively (a heterozygote will always have half the effect of a homozygote). However, for greatest realism, the majority of mutations should be made recessive, with a minority being dominant by default.">2. Mutations &mdash; dominant vs. recessive?</a></label>
      </div>

      <div id="crdiv">
        <div class="form-group">
          <label for="fraction_recessive" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="fraction_recessive" data-content="This parameter simply specifies the percentage of mutations that are recessive. If set to 0.8, then 80% of mutations are recessive, so the remaining 20% will automatically be made dominant.">a. fraction recessive (rest dominant):</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="fraction_recessive"
                   value="{{fraction_recessive}}" min="0" max="1" step="0.1"
                   id="fraction_recessive" class="form-control" title="0.0 - 1.0"
                   onchange="validate(this)">
          </div>
        </div>
        <div class="form-group">
          <label for="recessive_hetero_expression" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="recessive_hetero_expression" data-content=" It is widely believed that recessive mutations are not completely silent in the heterozygous condition, but are still expressed at some low level. Although the co-dominance default is 0.5 expression, a reasonable setting would be 0.05.">b. expression of recessive mutations (in heterozygote):</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="recessive_hetero_expression"
                   value="{{recessive_hetero_expression}}" class="form-control"
                   min="0" max="0.5" step="0.1" title="0.0 - 0.5"
                   onchange="validate(this)">
          </div>
        </div>
        <div class="form-group">
          <label for="dominant_hetero_expression" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="dominant_hetero_expression" data-content="It is widely believed that dominant mutations are not completely dominant in the heterozygous condition, but are only expressed only at some very high level. Although the co-dominance default is 0.5, a reasonable setting would be 0.95.">c. expression of dominant mutations (in heterozygote):</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="dominant_hetero_expression"
                   value="{{dominant_hetero_expression}}" class="form-control"
                   min="0.5" max="1.0" step="0.1" title="0.5 - 1.0"
                   onchange="validate(this)">
          </div>
        </div>
      </div>

      <hr>
      <div class="form-group">
        <label for="combine_mutns" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="combine_mutns" data-html="true" data-content='When there are two or more mutations within an individual, the effects of these multiple mutations must be combined. The most straightforward way to do this is additively, by just adding up the effects of all the deleterious and beneficial mutations within an individual, and adjusting original fitness (initially 1.0) by that net amount. Alternatively, one can adjust fitness by multiplying the fitness (initially 1.0) by the net effect of each mutation (the net effect of a single mutation would be one minus the fitness effect of that mutation). <a target="_blank" href="/static/apps/mendel/help.html#cmenam">Read more...</a>'>3. Combine mutations effects non-additively?</a></label>
        <div class="col-xs-2 col-sm-6">
          <input type="checkbox" name="combine_mutns"
                 onclick="fxn_combine_mutns()" value="on"
                  %if float(multiplicative_weighting) > 0:
                    checked
                  %end
          >
        </div>
      </div>

      <div id="mwdiv" style="display:none">
        <div class="form-group">
          <label for="multiplicative_weighting" class="control-label col-xs-12 col-sm-6">
                &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="multiplicative_weighting" data-content="For this input parameter, the researcher can select an all additive model (0.0 multiplicative = default), or an all multiplicative model (1.0, no additive component), or a mixed model having any intermediate value between 0 and 1.0. MENDEL’s default setting is the simple additive method. A third way to combine mutational effects is to use a synergistic epistasis model as shown below.">
                a. fraction multiplicative effect:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="multiplicative_weighting"
                   id="multiplicative_weighting" class="form-control"
                   value="{{multiplicative_weighting}}"
                   min="0" max="1" step="0.1"
                   onchange="onchange=validate(this)"
                   title="0.0 - 1.0">
          </div>
        </div>
      </div>

      <hr>

      <div class="form-group">
        <label for="synergistic_epistasis" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="synergistic_epistasis" data-html="true" data-content='In modeling synergistic epistasis (SE) in Mendel, we distinguish between SE contributions from deleterious mutation pairs which are linked together within a linkage block on a chromosome from those which are not. Linked mutations are inherited together, and therefore the SE effects of all their mutual interactions are as well. By contrast, genetic recombination progressively tends to scramble mutations that are not linked together. <a target="_blank" href="/static/apps/mendel/help.html#fslp">Read more...</a>'>
          4. Include mutation-mutation interactions (synergistic epistasis)?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="synergistic_epistasis"
                 value="on" onclick="fxn_synergistic_epistasis()"
                 %if synergistic_epistasis=='T':
                    checked
                 %end
          >
        </div>
      </div>
      <div class="form-group">
        <label for="se_nonlinked_scaling" class="control-label col-xs-12 col-sm-6">
           &nbsp;&nbsp;&nbsp;
           <a data-toggle="popover" title="se_nonlinked_scaling" data-html="true" data-content='Genetic recombination progressively tends to scramble mutations that are not linked together.  Hence, the total SE contribution from non-linked mutations has a transient component.  The SE effects arising from the non-linked interactions which change from one generation to the next act like a type of noise that interferes with the selection process. <a target="_blank" href="/static/apps/mendel/help.html#nonlinked_se">Read more...</a>'>a. scaling factor for non-linked SE interactions:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="se_nonlinked_scaling"
                 value="{{se_nonlinked_scaling}}" class="form-control"
                 min="0.0" max="1.0" step="0.1"
                 onchange="validate(this)" title="0.0 - 1.0" >
        </div>
      </div>

      <div class="form-group">
        <label for="se_linked_scaling" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="se_linked_scaling" data-html="true" data-content='We assume the amplitude of the linked SE effect of each pair-wise interaction to be proportional to the product of non-epistatic fitness effects of the two mutations in the pair. This means that if a mutation&rsquo;s effect on the non-mutant genome is small, then the SE contribution from its interactions with other mutations likewise is small. <a target="_blank" href="/static/apps/mendel/help.html#nonlinked_se">Read more...</a>'>b. scaling factor for linked SE interactions:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="se_linked_scaling"
                 value="{{se_linked_scaling}}" class="form-control"
                 min="0.0" max="1.0" step="0.1"
                 onchange="validate(this)" title="0.0 - 1.0" >
        </div>
      </div>

      <hr>

      <div class="form-group">
        <label for="allow_back_mutn" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="allow_back_mutn" data-content="In a large genome, the rate of back mutations (mutations that arise at nucleoside sides that have already mutated), is vanishingly small and of no consequence, but in small genomes (i.e., viruses), a significant fraction of the genome can become mutated, such that this parameter becomes useful.">5. Allow back mutations?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="allow_back_mutn"
                 value="on" onclick="check_back_mutn()"
                   %if allow_back_mutn=='T':
                    checked
                   %end
          >
        </div>
      </div>

      <div class="form-group">
        <hr>
        <label for="upload_mutations" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="upload_mutations" data-content="A specific set of mutations can be uploaded into the population before a run begins. When this option is selected a template is shown which can be used to identify mutations for uploading, or a set of mutations can be pasted into a template. This options is currently not implemented in this SPC version.">6. Upload set of custom mutations?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="upload_mutations"
                 value="on" onclick="show_hide_mutation_upload_form(1)"
                   %if upload_mutations=='T':
                    checked
                   %end
          >
        </div>
      </div>

    </div>

    <!--*************************** SELECTION TAB *******************************-->
    <div role="tabpanel" class="tab-pane fade" id="selection">

      <div class="form-group">
        <label for="fraction_random_death" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="fraction_random_death" data-content="A certain fraction of any population fails to reproduce, independent of phenotype. This can be expressed as the percentage of the population subject to random death. This is a useful parameter conceptually, but the same effect can be obtained by proportionately decreasing the number of offspring/female, so the default is zero.">1. Fraction of offspring lost apart from selection ("random death"):</a>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="fraction_random_death" class="form-control"
                 value="{{fraction_random_death}}"
                 min="0" max="0.99" step="0.1"
                 onchange="validate(this); compute_memory()"
                 title="0.0 - 0.99">
        </div>
      </div>

      <div class="form-group">
        <label for="heritability" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="heritability" data-content="Because a large part of phenotypic performance is affected by an individual’s circumstances (the “environment”), selection in nature is less effective than would be predicted simply from genotypic fitness values. Non-heritable environmental effects on phenotypic performance must be modeled realistically. MENDEL’s default value for the heritability is 0.2. This implies that on average, only 20% of an individual’s phenotypic performance is passed on to the next generation, with the rest being due to non-heritable factors. For a very general character such as reproductive fitness, 0.2 is an extremely generous heritability value. In most field contexts, it is in fact usually lower than this, typically being below the limit of detection.">2. Heritability:</a>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="heritability" title="0 - 1"
                 min="0" max="1" step="0.1"
                 onchange="validate(this)" class="form-control"
                 value="{{heritability}}">
        </div>
      </div>

      <div class="form-group">
        <label for="non_scaling_noise" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="non_scaling_noise" data-html="true" data-content='If a population’s fitness is increasing or declining, heritability (as calculated in the normal way), tends to scale with fitness, and so the implied “environmental noise” diminishes or increases as fitness diminishes or increases. This seems counter-intuitive. Also, with truncation selection, phenotypic variance becomes un-naturally small. For these reasons, it is desirable to model a component of environmental noise that does not scale with fitness variation. The units for this non-scaling noise parameter are based upon standard deviations from the initial fitness of 1.0. For simplicity, the default value is 0.05, but reasonable values probably exceed 0.01 and might exceed 0.1. <a target="_blank" href="/static/apps/mendel/help.html#nsn">Read more...</a>'>3. Non-scaling noise:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="non_scaling_noise" title="0 - 1"
                 min="0" max="1" step="0.1"
                 onchange="validate(this)" class="form-control"
                 value="{{non_scaling_noise}}">
        </div>
      </div>

      <div class="form-group">
        <label for="fitness_dependent_fertility" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="fitness_dependent_fertility" data-content='It is widely recognized that when fitness declines, fertility also declines. This in turn affects population surplus, which affects selection efficiency, and can eventually result in “mutational meltdown”. To model this, we have included an option wherein fertility declines proportional to the square of the fitness decline. The resulting fertility decline is initially very subtle, but becomes increasingly severe as fitness approaches zero.'>4. Fitness-dependent fecundity decline?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="fitness_dependent_fertility"
                 accesskey="4" value="on"
                 %if fitness_dependent_fertility=='T':
                    checked
                 %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="selection_scheme" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="selection_scheme" data-html="true" data-content='MENDEL’s default mode for type of selection is probability selection, wherein the probability of reproduction is proportional to an individual’s fitness ranking within the population. Two forms of probability selection are provided‐ classic and unrestricted.  In classic (textbook) probability selection, rather counter-intuitively, strict proportionality (relative to the most-fit individual) can combine with high average fitness and mild selection (low reproductive rates) to cause reductions in fitness and relatively rapid extinction.   In unrestricted probability selection, with certain combinations of average fitness and offspring/female, a range of the highest fitness values are “guaranteed” survival in order to maintain population size. <a target="_blank" href="/static/apps/mendel/help.html#ss">Read more...</a>'>5. Selection scheme:</a></label>
        <div class="col-xs-12 col-sm-3">
          <select id="selection_scheme" name="selection_scheme" accesskey="5"
                  class="form-control"  onchange="fxn_selection(this.value)">
            %opts = {'1': 'Truncation selection', '2': 'Unrestricted probability selection', '3': 'Strict proportionality probability selection', '4': 'Partial truncation selection'}
            %for key, value in sorted(opts.items()):
              %if key == selection_scheme:
                <option selected value="{{key}}">{{value}}
              %else:
                <option value="{{key}}">{{value}}
              %end
            %end
          </select>
        </div>
      </div>

      <div id="ptv">
        <div class="form-group">
          <label for="partial_truncation_value" class="control-label col-xs-12 col-sm-6">
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
               <a data-toggle="popover" title="selection_scheme" data-content='The partial truncation value, k, equals the fraction of the population which is truncated. If k=1, this is the same as full truncation selection. However, if k=0, this equals full probability selection. k=0.5 is the immediate blending of truncation and probability selection.'>a. partial truncation parameter, k</a></label>
          <div class="col-xs-12 col-sm-3">
              <input type="number" name="partial_truncation_value"
                  class="form-control" value="{{partial_truncation_value}}"
                  min="0" max="1" step="0.1"
                  onchange="validate(this)" title="0.0 - 1.0">
          </div>
        </div>
      </div>

    </div>

    <!--*************************** POPULATION TAB ******************************-->
    <div role="tabpanel" class="tab-pane fade" id="population">
      <div class="form-group">
        <label for="recombination_model" class="control-label col-xs-12 col-sm-6">
             <a data-toggle="popover" title="recombination_model" data-content='Normal sexual reproduction is the default setting, but clonal reproduction can be specified. If clonal reproduction is selected, there is no recombination, and the genome is treated as one large non-recombining chromosome. There is no mating, and the same genome is transmitted from female to offspring, with each offspring then being assigned its own set of new mutations.'>1. Recombination model:</a></label>
        <div class="col-xs-12 col-sm-3">
          <select id="recombination_model" name="recombination_model" class="form-control">
                  %opts = {'1': 'Clonal reproduction', '2': 'Suppressed recombination', '3': 'Full sexual recombination'}
                  %for key, value in sorted(opts.items()):
                      %if key == recombination_model:
                          <option selected value="{{key}}">{{value}}
                      %else:
                          <option value="{{key}}">{{value}}
                      %end
                  %end
          </select>
        </div>
       </div>

      <div class="form-group">
        <label for="fraction_self_fertilization" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="fraction_self_fertilization" data-content='Certain plants and lower animals can self-fertilize. The percentage of self-fertilization (as opposed to out-crossing) can be set to range from the default value 0%) up to 100%.  As this value increases, there is a strong increase in inbreeding and in the rate of mutation fixation.  Consequently, recessive loci have a much stronger effect on overall fitness than normal.'>2. Fraction self fertilization:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="fraction_self_fertilization" title="0 - 1"
                 value="{{fraction_self_fertilization}}" onchange="validate(this)"
                 min="0" max="1" step="0.1" class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="dynamic_linkage" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="dynamic_linkage" data-html="true" data-content='Because tracking every linkage block can become computationally expensive, the number of linkage blocks must be limited (default = 989, min=1, max=100,000). We also offer the researcher the option (turn off "dynamic linkage") of a simpler model involving the specification of a fixed number of linkage blocks and fully randomized recombination between all linkage blocks each generation (no chromosome number is required). <a target="_blank" href="/static/apps/mendel/help.html#dl">Read more...</a>'>3. Dynamic linkage?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="dynamic_linkage" accesskey="2"
                 value="on" onclick="fxn_dynamic_linkage()"
                 %if dynamic_linkage=='T':
                    checked
                 %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="haploid_chromosome_number" style="left:20px" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="haploid_chromosome_number" data-content='The number of linkage blocks is evenly distributed over a user-specified haploid number of chromosomes (default=23).  If dynamic linkage is turned off, this number is not required and will be disabled.'>a. haploid chromosome number:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="haploid_chromosome_number" title="1 - 100"
                 min="1" max="100" step="1" onchange="validate(this)" class="form-control"
                 value="{{haploid_chromosome_number}}">
        </div>
      </div>

      <div class="form-group">
        <label style="left:20px" class="control-label col-xs-12 col-sm-6">
          <a id="num_linkage_subunits" data-toggle="popover" title="num_linkage_subunits" data-content='Enter the number of linkage blocks. The number of linkage blocks should be an integer multiple of the number of chromosome (e.g. the default value of 989 is 43 times the default 23 chromosomes). MENDEL will automatically adjust to the nearest integer multiple (e.g. if you input 1000 and 23 chromosomes, MENDEL will use a value of 989).'>b. number of linkage subunits:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="num_linkage_subunits" title="1 - 10,000"
                 min="1" max="10000" data-warning="1000" step="1"
                 onchange="correct_lb(); fxn_auto_malloc(); validate(this)"
                 class="form-control" value="{{num_linkage_subunits}}">
        </div>
      </div>

      <div class="form-group">
        <label class="control-label col-xs-12 col-sm-6">
          4. Dynamic population size:</label>
      </div>

      <div class="form-group">
        <label for="pop_growth_model" style="left:20px" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="pop_growth_model" data-content='By default Mendel uses a static population size. However, two options are provided to simulate dynamic population growth: (1) exponential growth model (e.g. Figure 1), and (2) carrying-capacity model. For the exponential growth model, two additional inputs need to be entered: population growth rate and maximum population size.'>a. population growth model:</a></label>
        <div class="col-xs-12 col-sm-3">
          <select id="pop_growth_model" name="pop_growth_model" accesskey="5"
                  class="form-control"  onchange="fxn_pop_growth_model(this.value)">
            %opts = {'0': 'Off (fixed population size)', '1': 'Exponential growth', '2': 'Carrying capacity model', '3': 'Founder effects'}
            %for key, value in sorted(opts.items()):
              %if key == pop_growth_model:
                <option selected value="{{key}}">{{value}}
              %else:
                <option value="{{key}}">{{value}}
              %end
            %end
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="pop_growth_rate" style="left:20px" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="pop_growth_rate" data-content='The population growth rate parameter determines the percent growth rate per generation. A value of 1.0 represents static population size (no growth). To grow the population 2% per generation, enter the parameter 1.02 (note: one may need to manually convert published annual population growth rates to population growth per generation by using a formula such as 1.0220 = 1.48/generation — assuming a 20 year generation time).'>b. population growth rate:</a></label>
        <div class="col-xs-12 col-sm-3 input-group" style="padding-left:15px; padding-right:15px">
          <input type="number" name="pop_growth_rate" class="form-control"
                 min="1" max="10.0" step="0.02" onchange="validate(this)"
                 value="{{pop_growth_rate}}">
          <span class="input-group-addon"></span>
          <input type="number" name="pop_growth_rate2" class="form-control"
                 min="1" max="10.0" step="0.02" onchange="validate(this)"
                 value="{{pop_growth_rate2}}">
        </div>
      </div>

      <div class="form-group">
        <label for="carrying_capacity" style="left:20px" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="pop_growth_model" data-content='Mendel’s second population growth model is called “the carrying-capacity model”. Wikipedia.org gives the following definition for carrying capacity: “The supportable population of an organism, given the food, habitat, water and other necessities available within an environment is known as the environment’s carrying capacity for that organism.” The equation describing relating population growth to the environment’s carrying capacity can be given as: dN/dt = rN(K-N)/K [Reference: Halliburton, Richard. Introduction to Population Genetics, Benjamin Cummings, 2003]. where N is the population size, r is the maximum reproductive rate of an individual, and K is the carrying capacity.'>c. carrying capacity:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="carrying_capacity" class="form-control"
                 min="0" max="10000" step="100" onchange="validate(this)"
                 value="{{carrying_capacity}}">
        </div>
      </div>

      <div class="form-group">
        <label for="bottleneck_yes" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="bottleneck_yes" data-content='Population bottlenecks can dramatically affect mutation accumulation and mutation fixation.  MENDEL allows the modeling of population bottlenecks.   The researcher can cause a bottleneck to automatically begin after a specified number of generations, resulting in a specified reduction in population size, and ending after a specified number of bottleneck generations. The reduction of population size occurs immediately at the beginning of the bottleneck, by selecting a random sub-sample of the population. When the bottleneck ends, the original offspring number/female does not change but half of the population excess (i.e. all offspring exceeding 2 per female) is used to increase population size, and half of the excess continues to be eliminated by selection. When the original population size is reached, normal selection is restored.'>5. Bottleneck?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="bottleneck_yes" value="on"
                 class="checkbox" onclick="fxn_bottleneck()"
              % if bottleneck_yes == 'T':
                 CHECKED
              %end
            >
        </div>
      </div>

      <div id="bydiv" style="display:none">

        <div class="form-group">
          <label for="bottleneck_generation" class="control-label col-xs-12 col-sm-6">
               &nbsp;&nbsp;&nbsp;
               <a data-toggle="popover" title="bottleneck_generation" data-content='Enter the generation when the bottleneck starts.  To start the simulation with a bottleneck, enter a value of 0. To repeat a bottleneck every X generations, enter a negative value (e.g. -100 will repeat a bottleneck every 100 generations).'>a. generation when bottleneck starts:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="bottleneck_generation"
                   value="{{bottleneck_generation}}" class="form-control"
                   min="-50000" max="50000" step="10"
                   onchange="check_bottleneck(); validate(this)" title="2 - 50,000">
          </div>
        </div>

        <div class="form-group">
          <label for="bottleneck_pop_size" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="bottleneck_pop_size" data-content='Enter the population size during the bottleneck.'>b. population size during bottleneck:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" class="form-control" name="bottleneck_pop_size"
                   value="{{bottleneck_pop_size}}"  title="2 - 1,000">
          </div>
        </div>

        <div id="nbg" class="form-group">
          <label for="num_bottleneck_generations" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="num_bottleneck_generations" data-content='Enter the duration of the bottleneck in number of generations.'>c. duration of bottleneck - generations:</a></label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="num_bottleneck_generations" class="form-control"
                   min="1" max="5000" step="10" onchange="validate(this)"
                   value="{{num_bottleneck_generations}}" title="1 - 5,000">
          </div>
        </div>

      </div>

    </div>

    <!--*************************** SUBSTRUCTURE TAB ****************************-->
    <div role="tabpanel" class="tab-pane fade" id="substructure">

        <div class="form-group">
            <label for="is_parallel" class="control-label col-xs-10 col-sm-6">
            <a data-toggle="popover" title="is_parallel" data-content='Perfectly random mating within a population probably never happens, especially in larger dispersed populations. MENDEL allows creation of multiple sub-populations     (tribes), to account for this reality.'>Population substructure?</a></label>
            <div class="col-xs-2 col-sm-3">
                <input type="checkbox" name="is_parallel" onclick="fxn_is_parallel()"
                    value="on"
                    %if is_parallel=='T':
                        checked
                        %end
                        >
            </div>
        </div>

        <div id="psdiv" style="display:none">

            <div class="form-group">
              <label for="homogenous_tribes" class="control-label col-xs-10 col-sm-6">
                <a data-toggle="popover" title="homogenous_tribes" data-content='If this option is selected, all Mendel parameters will be applied to each single sub-population equally, so that all sub-populations will start out the same. If this is de-selected, each tribe can have its own parameters defined separately (currently not supported in this version).'>1. Homogeneous subpopulations?</a></label>
              <div class="col-xs-2 col-sm-3">
                <input type="checkbox" name="homogenous_tribes" readonly="true"
                       onclick="fxn_tribes(16)" value="on"
                       %if homogenous_tribes=='T':
                           checked
                       %end
                >
              </div>
            </div>

            <div class="form-group">
              <label for="num_procs" class="control-label col-xs-12 col-sm-6">
                <a data-toggle="popover" title="num_procs" data-content='The number of sub-populations (a.k.a. tribes or demes) can be specified here.  Each population is assigned to a separate process/thread on the CPU.'>2. Number of subpopulations:</a></label>
              <div class="col-xs-12 col-sm-3">
                <input type="number" id="num_procs" name="num_procs" class="form-control"
                       min="2" max="100" step="1" onchange="fxn_tribes(16)"
                       value="{{num_procs}}" title="2 - 100">
              </div>
            </div>

            <div class="form-group">
              <label for="migration_model" class="control-label col-xs-12 col-sm-6">
                <a data-toggle="popover" title="migration_model" data-content='One of three possible methods of migration can be selected: ring pass, stepping stone, and island models. The ring pass is the simplest mode of communications, and is typically used in testing parallel computing systems. In ring pass, the number of tribes are arranged as a circle, and each tribe sends the user-specified number of individuals to the neighbor to its right. In the stepping-stone model, the tribes are also arranged as a circle each tribe exchanges individuals with its neighber. In the island model, every tribe exchanges individuals with every other tribe.'>3. Migration model:</a></label>
                <div class="col-xs-12 col-sm-3">
                    <select class="form-control" id="migration_model" style="width:auto" name="migration_model">
                    %opts = {'1': 'Ring pass', '2': 'Stepping-stone model', '3': 'Island model'}
                    %for key, value in sorted(opts.items()):
                        %if key == migration_model:
                            <option selected value="{{key}}">{{value}}
                        %else:
                            <option value="{{key}}">{{value}}
                        %end
                    %end
                    </select>
                </div>
            </div>

            <div class="form-group">
              <label class="control-label col-xs-12 col-sm-6">
                <a data-toggle="popover" title="migration_model" data-content='The rate of migration can be specified. The rate of migration can be less than one (one migration event every X generations), and also can be zero.'>4. Migrate:</a></label>

                <div class="input-group col-xs-12 col-sm-3" style="width:320px; padding-left:15px">
                    <input class="form-control" type="number" name="num_indiv_exchanged"
                    title="1 to Pop Size" onchange="fxn_migration()";
                    min="1" size=2 value="{{num_indiv_exchanged}}">
                    <span class="input-group-addon">individual(s) per</span>
                    <input type="number" name="migration_generations" class="form-control"
                    min="1" size=2 value="{{migration_generations}}">
                    <span class="input-group-addon">gens</span>
                </div>
            </div>

            <div class="form-group">
                <label for="tribal_competition" class="control-label col-xs-10 col-sm-6">
                    <a data-toggle="popover" title="tribal_competition" data-html="true" data-content='Tribal competition can be specified (differential growth/shrinkage of tribes). Tribal competition works by first computing the global weighted average genetic fitness of all the tribes. Then, the tribal_fitness_factor is computed which is each tribes fitness relative to the global genetic fitness is computed. <a target="_blank" href="/static/apps/mendel/help.html#tc">Read more...</a>'>5. Competition between subpopulations?</a>
                </label>
                <div class="col-xs-2 col-sm-3">
                    <input type="checkbox" name="tribal_competition"
                    id="tribal_competition" onchange="fxn_tribes(16)" value="on"
                    %if tribal_competition=='T':
                    checked
                    %end
                    >
                </div>
            </div>

            <div class="form-group">
                <label for="tc_scaling_factor" class="control-label col-xs-12 col-sm-6">
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a data-toggle="popover" title="tc_scaling_factor" data-content='A scaling factor specifies the strength of tribal competition.
                    '>a. group selection scaling factor:</a>
                </label>
                <div class="col-xs-12 col-sm-3">
                    <input type="number" name="tc_scaling_factor" id="tc_scaling_factor"
                    min="0" max="1" step="0.1" onchange="validate(this)"
                    class="form-control" value="{{tc_scaling_factor}}"
                    title="0 - 1." readOnly=true>
                </div>
            </div>

            <div class="form-group">
                <label for="group_heritability" class="control-label col-xs-12 col-sm-6">
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a data-toggle="popover" title="group_heritability" data-content='Group heritability species the amount of environmental effect on differential tribal growth/shrinkage.'>b. group heritability:</a>
                </label>
                <div class="col-xs-12 col-sm-3">
                    <input type="number" name="group_heritability"
                    title="0-1, 0: max noise 1: no noise"
                    min="0" max="1" step="0.1" value="{{group_heritability}}"
                    onchange="validate(this)" class="form-control">
                </div>
            </div>

            <div class="form-group">
                <label for="altruistic" class="control-label col-xs-10 col-sm-6">
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a data-toggle="popover" title="altruistic" data-content='A specific set of mutations can be uploaded into the population before a run begins. When this option is selected a template is shown which can be used to identify mutations for uploading, or a set of mutations can be pasted into a template. This is currently not implemented in this version.'>c. upload altruistic mutations?</a>
            </label>
                <div class="col-xs-2 col-sm-3">
                    <input type="checkbox" name="altruistic" value="on"
                    onclick="show_hide_mutation_upload_form(2)">
                </div>
            </div>

            <div class="form-group" style="display:none">
              <label for="social_bonus_factor" class="control-label col-xs-12 col-sm-6">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                :: social bonus scaling factor:</label>
              <div class="col-xs-12 col-sm-3">
                <input type="number" style="width:7em;" name="social_bonus_factor"
                       class="form-control" min="0" max="1" step="0.1"
                       value="1.0" onchange="validate(this)" title="0 - 1">
              </div>
            </div>

            <div class="form-group">
              <label for="fission_tribes" class="control-label col-xs-10 col-sm-6">
                <a data-toggle="popover" title="fission_tribes" data-html="true" data-content='This option may be used for dynamically splitting a single tribe into one or more subtribes.'>6. Tribal Fissioning?</a></label>
              <div class="col-xs-2 col-sm-3">
                <input type="checkbox" name="fission_tribes" onclick="fxn_fission()"
                  id="fission_tribes" value="on"
                  %if fission_tribes=='T':
                     checked
                  %end
                >
              </div>
            </div>

            <div class="form-group">
                <label for="fission_type" class="control-label col-xs-12 col-sm-6">
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a data-toggle="popover" title="fission_type" data-content='(1) Competition - this is only valid in the context of group selection.  When one tribe dies, the winning tribe sends half of its individuals to the losing tribe. (2) Doubling - in the case of growing populations, when the tribe reaches a critical population size defined by the fission_threshold, it splits into two tribes. (3) Radial divergence - fission the tribe into N tribes (where N is the number of subpopulations) at a generation specified by the parameter fission_threshold.'>a. type of fission:</a>
                </label>
                <div class="col-xs-12 col-sm-3">
                    <select id="fission_type" name="fission_type"   class="form-control">
                    %opts = {'1': 'Competition', '2': 'Doubling', '3': 'Radial Divergence'}
                    %for key, value in sorted(opts.items()):
                        %if key == fission_type:
                            <option selected value="{{key}}">{{value}}</option>
                        %else:
                            <option value="{{key}}">{{value}}</option>
                        %end
                    %end
                    </select>
                </div>
            </div>

            <div class="form-group">
              <label for="fission_threshold" class="control-label col-xs-12 col-sm-6">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <a data-toggle="popover" title="fission_threshold" data-content='For the case of "doubling" this is the population size threshold.  For the case of "radial divergence", this is the generation number.  This value is not used for "competition" fissioning'>b. fission threshold:</a></label>
              <div class="col-xs-12 col-sm-3">
                <input type="number" name="fission_threshold" id="fission_threshold"
                       min="0" max="1000" step="100" onchange="validate(this)"
                       class="form-control" value="{{fission_threshold}}"
                       title="0 - 1000">
              </div>
            </div>

        </div>
    </div>

    <!--*************************** COMPUTATION TAB *****************************-->
    <div role="tabpanel" class="tab-pane fade" id="computation">

      <div class="form-group">
        <label for="auto_malloc" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="auto_malloc" data-content='By selecting this option, estimated values will be used for the maximum number of deleterious, favorable, and neutral mutations.  This estimation is simply computed by assuming a linear accumulation of mutations.  If this feature is turned off, the users can define the maximal number of mutations per individual manually.'>1. Automatically allocate memory?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="auto_malloc" value="on"
                 onclick="fxn_auto_malloc()"
                 %if auto_malloc=='T':
                    checked
                 %end
          >
        </div>
      </div>

      <div id="max_del_mutn_per_indiv" class="form-group">
        <label for="max_del_mutn_per_indiv" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="max_del_mutn_per_indiv" data-content='The maximum deleterious mutations per individual setting is how many deleterious mutations each individual can have. During a simulation, if this number is exceed the program will shutdown with an error that this number has been exceeded.'>a. maximum deleterious mutations per individual:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="max_del_mutn_per_indiv"
                   onchange="compute_memory(); validate(this)"
                   min="2" max="5000000" step="1000"
                   value="{{max_del_mutn_per_indiv}}" class="form-control">
        </div>
      </div>

      <div id="max_fav_mutn_per_indiv" class="form-group">
        <label for="max_fav_mutn_per_indiv" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="max_fav_mutn_per_indiv" data-content='The maximum favorable mutations per individual setting is how many favorable mutations each individual can have. During a simulation, if this number is exceed the program will shutdown with an error that this number has been exceeded.'>
          b. maximum favorable mutations per individual:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="max_fav_mutn_per_indiv" accesskey="0"
                     onchange="compute_memory(); validate(this)"
                     min="2" max="5000000" step="1000"
                     value="{{max_fav_mutn_per_indiv}}" class="form-control">
        </div>
      </div>

      <div id="max_neu_mutn_per_indiv" class="form-group">
        <label for="max_neu_mutn_per_indiv" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="max_neu_mutn_per_indiv" data-content='The maximum neutral mutations per individual setting is how many neutral mutations each individual can have. During a simulation, if this number is exceed the program will shutdown with an error that this number has been exceeded.'>
          c. maximum neutral mutations per individual:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="max_neu_mutn_per_indiv" accesskey="0"
                     onchange="compute_memory(); validate(this)"
                     min="2" max="5000000" step="1000"
                     value="{{max_neu_mutn_per_indiv}}" class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="track_neutrals" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="track_neutrals" data-content='Checking this box will set tracking threshold to zero, in which case all mutations will be tracked, including neutral mutations. This button must be checked if allele statistics are needed, or if neutral mutations are to be simulated.'>2. Track all mutations?</a><br>
          &nbsp;&nbsp;&nbsp;
          <font size="-1">(Note: must be checked if allele statistics
                           are needed)</font></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="track_all_mutn" value="on"
                 onclick="fxn_track_all_mutn()"
                 %if tracking_threshold==1:
                    checked
                 %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="tracking_threshold" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
            <a data-toggle="popover" title="tracking_threshold" data-html="true" data-content='MENDEL can track every individual mutation. However, this may not be the best choice, especially with large populations and/or large numbers of generations. Hundreds of millions of mutations can accumulate within a virtual MENDEL population, causing computer operating speed to slow to a crawl, and eventually exceeding all available memory. In order to speed operation and allow larger experiments, MENDEL can track only those individual mutations that are “potentially meaningful”. Most mutational effects are so close to zero, that they can be classified as “extremely near-neutral”. Such effects are so extremely small that they have no significant impact, even after accumulating to very high numbers for many, many generations. <a target="_blank" href="/static/apps/mendel/help.html#tt">Read more...</a>'>:: To conserve memory and speed up runs, <br> &nbsp;&nbsp;&nbsp;
            do not track mutations with fitness effects less than:</a>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="tracking_threshold"
                 onchange="validate(this)" class="form-control"
                 min="0" max="1" step="0.0001"
                 title="1e-4 ~ 1e-8" value="{{tracking_threshold}}">
        </div>
      </div>

      <div class="form-group">
        <label for="extinction_threshold" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="extinction_threshold" data-content='Extinction can either be realized when fitness reaches the specified extinction threshold value -or- by population size dropping to a value of one. The default for fitness extinction threshold is 0.0.'>3. Go extinct when mean fitness reaches:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="extinction_threshold"
                 min="0" max="1" step="0.1"
                 onchange="validate(this)" class="form-control"
                 title="0-1" value="{{extinction_threshold}}">
        </div>
      </div>

      <div class="form-group">
        <label for="random_number_seed" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="random_number_seed" data-content='At several stages within the MENDEL program, a random number generator is required. When an experiment needs to be independently replicated, the “random number seed” must be changed. If this is not done, the second experiment will be an exact duplicate of the earlier run.'>4. Random number generator (RNG) seed:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="random_number_seed" title="1 - 1000"
                 min="1" max="1e9" step="1" onchange="validate(this)"
                 class="form-control" value="{{random_number_seed}}">
        </div>
      </div>

      <div class="form-group">
        <label for="reseed_rng" class="control-label col-xs-10 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="reseed_rng" data-content='This option can be used to add even more randomness into the simulation. It is generally thought that using an XOR of the process ID (PID) and the time will create a unique random number seed every time.'>:: Reseed the RNG every gen using PID&#8853;Time:</a><br>
          &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
          <font size="-1">(Warning: if checked, runs will not be repeatable)</font>
        </label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="reseed_rng" value="on"
            %if reseed_rng=='T':
               checked
            %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="write_dump" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="write_dump" data-content='MENDEL allows a run to go for a specified number of generations, followed by data output, alteration of certain biological parameters, and resumption of the run. This can be done repeatedly, simply by choosing the commands allow this run to be re-started prior to a run, and then later restart new phase of run prior to subsequent runs.   Most parameters can be altered at restart, but population size and the number of linkage blocks must remain unchanged.  (Caution: allowing restarts of large runs will save large amounts of data, which can rapidly fill available disk storage.).'>5. Allow this run to be later re-started with new parameters?</a><br>
          <font size="-1">&nbsp;&nbsp;&nbsp;&nbsp;
          (Note: these restart files are very large ~1GB)</font></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="write_dump" accesskey="3" value="on"
              %if write_dump=='T':
                 checked
              %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="restart_case" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="restart_case" data-content='Check this button in order to use the data from a previously run case (a case that has previously been run with the “Allow this run to be later re-started...” button checked).'>6. Restart second (third, fourth) phase of run
             with these new parameters?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="restart_case" accesskey="4"
            onclick="fxn_restart_case()" value="on"
            %if restart_case=='T':
                checked
            %end
          >
        </div>
      </div>

      <div id="rddiv" style="display:none">

        <div class="form-group">
          <label for="restart_dump_number" class="control-label col-xs-12 col-sm-6">
            &nbsp;&nbsp;&nbsp; a. restart from which phase of run:</label>
          <div class="col-xs-12 col-sm-3">
            <input type="number" name="restart_dump_number" title="1 - 100"
                   min="1" max="100" step="1" onchange="validate(this)"
                   value="{{restart_dump_number}}" class="form-control">
          </div>
        </div>

        <div class="form-group">
          <label for="restart_case_id" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; b. restart from which case ID:</label>
          <div class="col-xs-12 col-sm-3">
            <input type="text" name="restart_case_id"
                   title="must be six letters" value="{{restart_case_id}}">
          </div>
        </div>

        <div class="form-group">
          <label for="restart_append" class="control-label col-xs-10 col-sm-6">
            &nbsp;&nbsp;&nbsp; c. append data to previous case:</label>
          <div class="col-xs-2 col-sm-3">
            <input type="checkbox" name="restart_append" value="on"
              %if restart_append=='T':
                  CHECKED
              %end
            >
          </div>
        </div>

      </div>

      <div class="form-group">
        <label for="plot_allele_gens" class="control-label col-xs-12 col-sm-6">
            <a data-toggle="popover" title="plot_allele_gens" data-content='Input the time interval (number of generations) that MENDEL will perform a polymorphism analysis of allele frequencies. Polymorphisms analysis requires cycling through all the mutations, so it is computationally expensive. Reducing this number will cause MENDEL to update the Allele Frequencies plot more often, but will also cause MENDEL to run for a longer amount of time. The default is computation of allele frequencies every 100 generations.'>7. Compute allele frequencies every:</a></label>
        <div class="input-group col-xs-12 col-sm-3" style="width:200px; padding-left:15px">
          <input type="number" name="plot_allele_gens"
                 class="form-control" min="1" max="10000" step="1"
                 onchange="validate(this)"
                 title="0-1" value="{{plot_allele_gens}}">
          <span class="input-group-addon">gens</span>
        </div>
      </div>

      <div class="form-group">
        <label for="verbosity" class="control-label col-xs-12 col-sm-6">
          <a data-toggle="popover" title="verbosity" data-content='MENDEL generates a lot of output information. However, not all of it is necessary. This verbosity option allows the user to limit the amount of files that are written to disk in order to save hard disk space. A verbosity level of 0 will essentially turn most diagnostics routines off, and will output just a .out output file and a .hst history file (which will allow viewing of fitness and mutation plots). A verbosity level of 1 will write all necessary files for plotting using the default JavaScript plotting system (Flot). A verbosity level of 2 "Output everything" is required to write ancillary files, such as .gnu Gnuplot files, .tim timing information for performance benchmarking, .pmd polymorphism frequency table, .acc table of accumulated deleterious dominant mutations, etc.'>8. Output verbosity level:</a></label>
        <div class="col-xs-12 col-sm-3">
          <select name="verbosity" class="form-control" id="verbosity">
            %opts = {'0': '0-Output only history', '1': '1-Output necessary files', '2': '2-Output everything' }
            %for key, value in sorted(opts.items()):
                %if key == verbosity:
                    <option selected value="{{key}}">{{value}}
                %else:
                    <option value="{{key}}">{{value}}
                %end
            %end
           </select>
          </div>
      </div>


      <div class="form-group">
          <label for="write_vcf" class="control-label col-xs-10 col-sm-6">
              <a data-toggle="popover" title="global_allele_analysis" data-html="true" data-content=''>
              9. Global allele analysis?</a>
          </label>
          <div class="col-xs-2 col-sm-3">
              <input type="checkbox" name="global_allele_analysis" accesskey="4" value="on"
              %if global_allele_analysis=='T':
                 checked
              %end
              >
          </div>
      </div>

      <div class="form-group">
        <label for="write_vcf" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="write_vcf" data-html="true" data-content='Selecting this option will output a very large VCF file which will contain every allele in the population, which can then be analyzed by a number of other programs (e.g. vcftools, gatk, etc.) <a target="_blank" href="https://en.wikipedia.org/wiki/Variant_Call_Format">Read more about VCF files...</a>'>
          10. Output Allele File?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="write_vcf" onclick="fxn_write_alleles()" value="on"
            %if write_vcf=='T':
                checked
            %end
          >
        </div>
      </div>

    </div>

    <!--*********************** SPECIAL APPLICATIONS TAB *************************-->
    <div role="tabpanel" class="tab-pane fade" id="special">

      <div class="form-group">
        <label class="control-label col-xs-12 col-sm-6">
            <a data-toggle="popover" title="initial_alleles" data-content='This means that the population starts with pre-existing diversity. This feature is still under development and largely untested. The user must specify the number of initial contrasting alleles, and the total fitness increase - if all favored alleles go to fixation.'>1. Initial heterozygous alleles (ICA):</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="initial_alleles" onclick="fxn_initial_alleles(this.value)"
            %if track_neutrals=='T':
            checked
            %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="num_contrasting_alleles" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="num_contrasting_alleles" data-html="true" data-content='This input lets the researcher begin a run with a specified number of initial contrasting alleles (heterozygous alleles), with a positive and negative allele at each contrasting locus in each individual. This gives an initial frequency of 50% for each allele, where each allele is co-dominant. This situation is analogous to an F1 population derived from crossing two pure lines or two relatively uniform breeding lines of animals, and is very roughly analogous to natural crossing of two isolated populations in nature. This input allows investigation of the effect of factors such as environmental variability, type of selection, and percent selfing on the retention of beneficial alleles during segregation after a cross. <a target="_blank" href="/static/apps/mendel/help.html#nca">Read more...</a>'>
          a. number of initial contrasting alleles:</a><br>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="num_contrasting_alleles" title="1 - 1000"
                 min="1" max="1000" step="1" value="{{num_contrasting_alleles}}"
                 onchange="alpha_warning(); validate(this)" class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="max_total_fitness_increase" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="max_total_fitness_increase" data-html="true" data-content='The maximum total fitness increase is the amount the fitness which would be increased if all the positive alleles became fixed (homozygous in every individual). Realistically, this value would always be considerably less than 1. A value of 1 would potentially double the mean fitness (“yield” in plant breeding situations). Such a large potential increase would be larger than most situations encountered in nature or in plant or animal breeding. The actual fitness increase in the population will actually always be less than the maximum total fitness increase (unless selection moved all the positive alleles to fixation). <a target="_blank" href="/static/apps/mendel/help.html#mtfi">Read more...</a>'>b. maximum total fitness increase:</a><br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <font size="-1">Note: this value must be &gt; 0 for ICA to work.</font> </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="max_total_fitness_increase" title="0 - 1"
              value="{{max_total_fitness_increase}}" min="0" max="1" step="0.1"
              onchange="validate(this)"
              class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="initial_alleles_pop_frac" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="initial_alleles_pop_frac" data-content='This is the fraction of the population which has the allele. For example, for 50% of the population to have the allele, specify 0.5 here.'>c. fraction of population which has allele:</a><br>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="initial_alleles_pop_frac" title="0 - 1"
              value="{{initial_alleles_pop_frac}}" min="0" max="1" step="0.1"
              onchange="validate(this)"
              class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="num_high_impact_alleles" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="num_high_impact_alleles" data-content=''>d. number of high impact alleles:</a><br>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="num_high_impact_alleles" title="0 - 1"
              value="{{num_high_impact_alleles}}" min="0" max="1000" step="0.1"
              onchange="validate(this)"
              class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="high_impact_amplitude" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="high_impact_amplitude" data-content=''>e. amplitude of high impact mutations:</a><br>
        </label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="high_impact_amplitude" title="0 - 1"
              value="{{high_impact_amplitude}}" min="0" max="1" step="0.1"
              onchange="validate(this)"
              class="form-control">
        </div>
      </div>

      <div class="form-group">
        <label for="track_neutrals" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="track_neutrals" data-html="true" data-content='This means that a specified fraction of all new mutations will arise within the “junk DNA” portions of the genome, and so will be perfectly neutral. If 50% of the genome is junk, then 50% of all mutations will be neutral. If the total mutation rate is 100 per generation, then the rate of neutral mutations will be 50 per generation. The remaining non-neutral mutations will have the specified benefical-to-deleterious mutation rate. Neutral mutations will then be tracked, tallied, and plotted, just as with beneficial and deleterious mutations. <a target="_blank" href="/static/apps/mendel/help.html#fraction_neutral">Read more...</a>'>2. Include neutrals in analysis:</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="track_neutrals" onclick="fxn_track_neutrals()"
            %if track_neutrals=='T':
            checked
            %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="fraction_neutral" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp;
          <a data-toggle="popover" title="fraction_neutral" data-html="true" data-content='It is not clear that any mutations are perfectly neutral, but in the past it has often been claimed that most of the human genome is non-function “junk DNA”, and that mutations in these regions are truly neutral. For the human default, we allow (but do not believe) that 90% of the genome is junk DNA, and so 90% of all human mutations have absolutely no biological effect. Because of the computational cost of tracking so many neutral mutations we specify zero neutrals be simulated, and discount the mutation rate so it only reflects non-neutral mutations (see above). <a target="_blank" href="/static/apps/mendel/help.html#fmun">Read more...</a>'>a. fraction of genome which is non-functional <em>junk</em>:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="fraction_neutral" id="fmun"
                 value="{{fraction_neutral}}" class="form-control"
                 min="0" max="1" step="0.1"
                 onchange="fxn_fraction_neutral(); fxn_auto_malloc(); validate(this)"
                 title="0 - 1">
          <table class="table">
             <tr><td>neutral mutation rate:</td> <td><code><span id="uneu"></span></font></code></td> </tr>
          </table>
        </div>
      </div>

      <div class="form-group">
        <label for="polygenic_beneficials" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="polygenic_beneficials" data-html='true' data-content='MENDEL can determine the waiting time required to establish specific beneficial nucleotides or nucleotide strings. The user must specify the initialization sequence (such as AAAA), and the target sequence (such as GTCT). The user must the degree of benefit (a fitness benefit of 1% is designated as 0.01). <a target="_blank" href="/static/apps/mendel/help.html#adv_wait">Read more...</a>'>3. Waiting time experiments?</a></label>
        <div class="col-xs-2 col-sm-3">
          <input type="checkbox" name="polygenic_beneficials"
                     title="" onclick="fxn_polygenic_beneficials()"
            %if polygenic_beneficials=='T':
              checked
            %end
          >
        </div>
      </div>

      <div class="form-group">
        <label for="polygenic_init" class="control-label col-xs-6 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="polygenic_init" data-html='true' data-content='Initialize every individual with this sequence <a target="_blank" href="/static/apps/mendel/help.html#adv_wait">Read more...</a>'>a. initialization sequence:</a></label>
        <div class="col-xs-6 col-sm-3">
          <input type="text" name="polygenic_init" id="polygenic_init"
                 value="{{polygenic_init}}" class="form-control"
                 onchange="fxn_polygenic_target()" title="e.g. AAAAA">
        </div>
      </div>

      <div class="form-group">
        <label for="polygenic_target" class="control-label col-xs-6 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="polygenic_target" data-html='true' data-content='This is the target sequence.  For each instance that this target is reached by random mutation, a beneficial fitness effect specified in the next entry is added to the individual&rsquo;s total fitness <a target="_blank" href="/static/apps/mendel/help.html#adv_wait">Read more...</a>'>b. target sequence:</a></label>
        <div class="col-xs-6 col-sm-3">
          <input type="text" name="polygenic_target" id="pbnr"
                 value="{{polygenic_target}}" class="form-control"
                 title="e.g. TCGTCG">
        </div>
      </div>

      <div class="form-group">
        <label for="polygenic_effect" class="control-label col-xs-12 col-sm-6">
          &nbsp;&nbsp;&nbsp; <a data-toggle="popover" title="polygenic_effect" data-html='true' data-content='Each time a target is found, add this fitness effect to the individual&rsquo;s total fitness. <a target="_blank" href="/static/apps/mendel/help.html#adv_wait">Read more...</a>'>c. fitness effect associated with target:</a></label>
        <div class="col-xs-12 col-sm-3">
          <input type="number" name="polygenic_effect" id="pbnr" class="form-control"
                 min="0" max="1" step="0.001" onchange="validate(this)"
                 value="{{polygenic_effect}}" title="0.0-1.0">
        </div>
      </div>

      <div class="form-group">
        <label for="special_feature_code" class="control-label col-xs-10 col-sm-6">
          <a data-toggle="popover" title="special_feature_code" data-html='true' data-content=''>4. Special feature code?</a></label>
        <div class="col-xs-2 col-sm-3">
            <input type="number" name="special_feature_code" class="form-control"
                   min="0" max="100000" step="1" onchange="validate(this)"
                   value="{{special_feature_code}}" title="0 - 100000">
        </div>
      </div>

    </div>

  </div>
  <!--*********************** END TAB CONTENT *************************-->

  <div id="upload_mutations_div" class="panel panel-primary" style="display:none">
      <div class="panel-heading">
          <h3 class="panel-title">Upload Mutations</h3>
      </div>
      <div class="panel-body" align="center">
          <div class="btn-group">
              <font size="+1">
                <a class="btn btn-warning" href="/static/apps/mendel/upload_mutations.xlsx"><span class="glyphicon glyphicon-cloud-download"></span> download worksheet</a>
                <button type="button" class="btn btn-info" data-toggle="modal" data-target="#upload_modal" ><span class="glyphicon glyphicon-cloud-upload"></span> upload mutations</button>
                <span class="text-success" id="upload_status"></span>
              </font>
          </div>
          <input type="hidden" name="mutn_file_id" style="width:7em;"
                     title="Currently this filename cannot be changed"
                     readOnly="true">
      </div>
  </div>

  <input type="hidden" name="data_file_path" value="{{data_file_path}}">
  <br>

  <div class="visible-xs col-xs-12">
    <button type="submit" class="btn btn-success"> <!-- pull-right -->
      Continue <em class="glyphicon glyphicon-forward"></em> </button>
  </div>

  <div class="row">
      <div class="form-group">
        <div class="hidden-xs col-sm-10 col-sm-offset-1">
          <input type="text" id="desc" name="desc" class="form-control"
                 data-role="tagsinput" placeholder="enter tag...">
        </div>
      </div>
  </div>

  </form>

</div> <!-- container-fluid -->

<div class="modal fade" id="upload_modal" tabindex="-1" role="dialog" aria-labelledby="" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="">Paste in mutations to upload</h4>
            </div>
            <div class="modal-body">
                <p> Note: the mutation table should have the following form:</p>

                <table>
                    <tr>
                        <th><label title="1 to pop_size">individual</label></th>
                        <th><label title="1 to num_linkage_blocks">linkage_block</label></th>
                        <th><label title="1 or 2">hap_id</label></th>
                        <th><label title="0.00001~1\n+ beneficial\n- deleterious">fitness</label></th>
                        <th><label title="+1:dominant\n-1:recessive">dominance</label></th>
                        <tr><td>1 to pop_size</td><td>1 to num_linkage_blocks</td> <td>1 or 2</td> <td>+/-0.000001 to +/-1<br>-: deleterious<br>+:favorable</td><td>-1 or 1<br>1:dominant<br>-1:recessive</td></tr>
                    </tr>
                </table>

                <p>Also, there should <u>not</u> be a header row. So, for example:</p>

                <table>
                    <tr><td>56</td> <td>407</td> <td>2</td> <td>-0.000117976</td><td>1</td></tr>
                </table>

                <form class="form-group">
                    <label for="chromosome_range" class="control-label col-xs-12 col-sm-3"><a data-toggle="popover" title="chromosome_range" data-content="List of chromosomes with min of 1 and max of 23. Can be comma-separated list such as: 1, 3, 5.  Or a range, such as: 1-23.  Or can be combination of both, e.g. 1, 3, 5, 7-10">List of Chromosomes</a></label>
                    <div class="col-xs-12 col-sm-6">
                        <input id="chromosome_range" class="form-control input-lg col-xs-3" />
                        <label>contrasting:</label> <input type="checkbox" id="contrasting" />
                        <select id="contrast_degree">
                            <option>1:1</option>
                            <option>1:3</option>
                        </select>
                    </div>
                    <div class="col-xs-12 col-sm-3">
                        <a class="btn btn-primary" href="javascript:generate_mutations()">Generate</a>
                    </div>
                </form>

                <p align="center" style="line-height:20px"> <span class="text-success" id="gen_stats"></span> </p>

                <form id="upload_mutations" name="upload_mutations_form" method=post action="/upload_data">
                    <textarea id="payload" class="form-control" name="upload_data" rows="7" style="font-family: monospace"></textarea><br />
                    <input type="hidden" name="filename" value="mendel.mutn">
                    <a class="btn btn-success center-block" href="javascript:UploadData()">Upload</a>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
  $(document).ready(function() {
    fxn_init();
    $('#desc').tagsinput('add', 'v2.7.1');
    %if defined('tags'):
      $('#desc').tagsinput('add', '{{tags}}');
    %end
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();
  })

  function UploadData() {
      data = document.getElementById("payload").value
      $.post( "/upload_data", { filename: "mendel.mutn", upload_data: data } )
      $('#upload_status').html("<span class=\"glyphicon glyphicon-ok\"></span> mutations uploaded")
      $('#upload_modal').modal('hide');
  }

  $('[data-toggle="popover"]').popover({ container: 'body' })

  dmi = document.mendel_input;
  //fxn_synergistic_epistasis_disable();
  document.getElementById("ptv").style.display = "none";
  dmi.pop_growth_rate.readOnly = false;
  dmi.num_contrasting_alleles.readOnly = false;
  dmi.max_total_fitness_increase.readOnly = false;
  // set select option boxes with proper values
  document.getElementById('fitness_distrib_type').value={{fitness_distrib_type}};
  document.getElementById('selection_scheme').value={{selection_scheme}};
  document.getElementById('pop_growth_model').value={{pop_growth_model}};
  document.getElementById('migration_model').value={{migration_model}};
</script>

{% include "footer.tpl" %}
