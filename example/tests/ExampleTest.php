<?php

namespace Example\Tests;

use Example\Example;
use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    public function testDoSomething()
    {
        $example = new Example();

        $this->assertTrue($example->doSomething(500));
    }
}
