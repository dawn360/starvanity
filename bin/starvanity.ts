#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { StarvanityStack } from '../lib/starvanity-stack';

const app = new cdk.App();
new StarvanityStack(app, 'StarvanityStack');
