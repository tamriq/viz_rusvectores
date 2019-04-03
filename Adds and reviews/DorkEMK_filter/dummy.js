// imitation of model results
var list_value = {'ruwikiruscorpora_upos_skipgram_300_2_2019': {'пирога': [79804, 'mid'], 'пирожок': [7222, 'high'], 'торт': [149222, 'mid'], 'ватрушка': [2973, 'low'], 'лепешка': [3789, 'low'], 'жареный': [28454, 'mid'], 'кулебяка': [142759, 'low'], 'суп': [27306, 'high'], 'пирожное': [6261, 'mid'], 'сырник': [2459, 'low'], 'десерт': [44029, 'mid'], 'булочка': [20172, 'mid'], 'пбиточек': [628, 'low'], 'фрикаделька': [484, 'low']}}

// пересобирает результат так, что каждой частоте соответствует массив результатов
function makeListForEachFilter(frequencies){
  let allFrequencies = {}
  for (const model in frequencies){
    allFrequencies[model] ={};
    allFrequencies[model].freq = {};
    allFrequencies[model].freq.high=[];
    allFrequencies[model].freq.mid=[];
    allFrequencies[model].freq.low=[];
  
  for (word in frequencies[model]){
      if (frequencies[model][word][1] == 'high'){
        allFrequencies[model].freq.high.push(word);
      } else if (frequencies[model][word][1] == 'mid'){
        allFrequencies[model].freq.mid.push(word);
      } else {allFrequencies[model].freq.low.push(word);
      };
    };
    };
  console.log(allFrequencies)
  return allFrequencies;
};

// показывает не более 10 результатов
// выдаёт не массив, а <li> если его текст входит в массив
// т.к.элементы массива не сортированы по similarity
function formResultsUsingFilterList(array){
  let counter = 0
  $("li").each(function(){
      if ($.inArray($(this).text().trim(), array) > -1 && counter <10){
      $(this).fadeIn('slow');
      counter ++;
      } else {
        $(this).fadeOut('slow');
      };
    });
};

// смотрим на чекбоксы и по ним формируем массив подходящих слов
function checkFrequencyMakeOutput(){
  const frequencies = ['high', 'mid', 'low'];
  const allFilters = (makeListForEachFilter(list_value));
  let resultChecked = [];
  $.each(frequencies, function(index,value){
    if ($("#"+value).is(':checked')){
      $.each(allFilters, function(model,data){
        $.each(data, function(filter, list){
          resultChecked = resultChecked.concat(allFilters[model][filter][value]);
        });
      });
    };
  });
  console.log(resultChecked)
  formResultsUsingFilterList(resultChecked)
};

// проверяем чекбоксы при запуске страницы и при любом клике
  $(document).ready(function(){
    checkFrequencyMakeOutput();
    $(".checkbox").change(function(){
      checkFrequencyMakeOutput();
    });
  });
